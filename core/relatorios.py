from datetime import datetime
import os

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)

from .models import Financeiro


# ==========================================================
# ESTILOS
# ==========================================================

styles = getSampleStyleSheet()

titulo = styles["Heading1"]
titulo.fontName = "Helvetica-Bold"
titulo.fontSize = 22
titulo.textColor = colors.HexColor("#0F172A")
titulo.alignment = TA_CENTER

subtitulo = styles["Heading2"]
subtitulo.fontName = "Helvetica"
subtitulo.fontSize = 10
subtitulo.textColor = colors.HexColor("#64748B")
subtitulo.alignment = TA_CENTER

texto = styles["BodyText"]
texto.fontName = "Helvetica"
texto.fontSize = 9
texto.leading = 15
texto.alignment = TA_LEFT


# ==========================================================
# RELATÓRIO FINANCEIRO
# ==========================================================

def gerar_relatorio_financeiro(request):

    financeiro = Financeiro.objects.all()

    tipo = request.GET.get("tipo")
    categoria = request.GET.get("categoria")
    busca = request.GET.get("busca")
    forma_pagamento = request.GET.get("forma_pagamento")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    if tipo:
        financeiro = financeiro.filter(tipo=tipo)

    if categoria:
        financeiro = financeiro.filter(
            categoria__icontains=categoria
        )

    if busca:
        financeiro = financeiro.filter(
            descricao__icontains=busca
        )

    if forma_pagamento:
        financeiro = financeiro.filter(
            forma_pagamento=forma_pagamento
        )

    if data_inicio:
        financeiro = financeiro.filter(
            data_movimentacao__gte=data_inicio
        )

    if data_fim:
        financeiro = financeiro.filter(
            data_movimentacao__lte=data_fim
        )

    entradas = financeiro.filter(
        tipo="ENTRADA"
    ).aggregate(
        Sum("valor")
    )["valor__sum"] or 0

    saidas = financeiro.filter(
        tipo="SAIDA"
    ).aggregate(
        Sum("valor")
    )["valor__sum"] or 0

    saldo = entradas - saidas

    quantidade = financeiro.count()

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="financeiro_gestcar.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        rightMargin=1.2 * cm,
    )

    elementos = []
    
        # ==========================================================
    # LOGO
    # ==========================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "core",
        "static",
        "img",
        "logo.png"
    )

    logo = None

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=1.7 * cm,
            height=1.7 * cm
        )

    # ==========================================================
    # CABEÇALHO
    # ==========================================================

    if logo:

        cabecalho = Table(
            [[
                logo,
                Paragraph(
                    """
                    <font size="20">
                    <b>GestCar Pro</b>
                    </font><br/>

                    <font size="10" color="#64748B">
                    Sistema de Gestão para Estética Automotiva
                    </font>
                    """,
                    texto
                )
            ]],
            colWidths=[
                2.2 * cm,
                14.5 * cm
            ]
        )

    else:

        cabecalho = Table(
            [[
                "",
                Paragraph(
                    """
                    <font size="20">
                    <b>GestCar Pro</b>
                    </font><br/>

                    <font size="10" color="#64748B">
                    Sistema de Gestão para Estética Automotiva
                    </font>
                    """,
                    texto
                )
            ]],
            colWidths=[
                2.2 * cm,
                14.5 * cm
            ]
        )

    cabecalho.setStyle(

        TableStyle([

            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),

        ])

    )

    elementos.append(cabecalho)

    elementos.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    elementos.append(

        Paragraph(

            "<b>RELATÓRIO FINANCEIRO</b>",

            subtitulo

        )

    )

    elementos.append(

        Paragraph(

            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            ),

            texto

        )

    )

    elementos.append(
        Spacer(
            1,
            0.8 * cm
        )
    )
    
        # ==========================================================
    # INDICADORES
    # ==========================================================

    cards = [[

        Paragraph(
            f"""
            <font color="#16A34A" size="9">
            <b>ENTRADAS</b>
            </font><br/><br/>
            <font size="18">
            <b>R$ {entradas:,.2f}</b>
            </font>
            """,
            texto
        ),

        Paragraph(
            f"""
            <font color="#DC2626" size="9">
            <b>SAÍDAS</b>
            </font><br/><br/>
            <font size="18">
            <b>R$ {saidas:,.2f}</b>
            </font>
            """,
            texto
        ),

        Paragraph(
            f"""
            <font color="#2563EB" size="9">
            <b>SALDO</b>
            </font><br/><br/>
            <font size="18">
            <b>R$ {saldo:,.2f}</b>
            </font>
            """,
            texto
        ),

        Paragraph(
            f"""
            <font color="#F59E0B" size="9">
            <b>MOVIMENTAÇÕES</b>
            </font><br/><br/>
            <font size="18">
            <b>{quantidade}</b>
            </font>
            """,
            texto
        ),

    ]]

    tabela_cards = Table(
        cards,
        colWidths=[
            4.3 * cm,
            4.3 * cm,
            4.3 * cm,
            4.3 * cm,
        ],
        rowHeights=[
            2.6 * cm
        ]
    )

    tabela_cards.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.white),

            ("BOX",(0,0),(-1,-1),0.35,colors.HexColor("#D1D5DB")),

            ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#E5E7EB")),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("BOTTOMPADDING",(0,0),(-1,-1),14),

            ("TOPPADDING",(0,0),(-1,-1),14),

            ("LEFTPADDING",(0,0),(-1,-1),12),

            ("RIGHTPADDING",(0,0),(-1,-1),12),

        ])

    )

    elementos.append(tabela_cards)

    elementos.append(
        Spacer(
            1,
            0.8 * cm
        )
    )

    # ==========================================================
    # RESUMO
    # ==========================================================

    elementos.append(
        Paragraph(
            "<b>Resumo do Relatório</b>",
            styles["Heading2"]
        )
    )

    resumo = f"""
    <br/>
    <b>Período:</b> {data_inicio or "Todos"} até {data_fim or "Hoje"}<br/>
    <b>Categoria:</b> {categoria or "Todas"}<br/>
    <b>Forma de pagamento:</b> {forma_pagamento or "Todas"}<br/>
    <b>Total de registros:</b> {quantidade}
    """

    elementos.append(
        Paragraph(
            resumo,
            texto
        )
    )

    elementos.append(
        Spacer(
            1,
            0.8 * cm
        )
    )

    elementos.append(
        Paragraph(
            "<b>Movimentações Financeiras</b>",
            styles["Heading2"]
        )
    )

    elementos.append(
        Spacer(
            1,
            0.4 * cm
        )
    )
    
        # ==========================================================
    # TABELA
    # ==========================================================

    dados = [[
        "Data",
        "Tipo",
        "Descrição",
        "Categoria",
        "Pagamento",
        "Valor"
    ]]

    for mov in financeiro.order_by("-data_movimentacao"):

        valor = f"R$ {mov.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        if mov.tipo == "ENTRADA":
            valor = f"<font color='#16A34A'><b>+ {valor}</b></font>"
        else:
            valor = f"<font color='#DC2626'><b>- {valor}</b></font>"

        dados.append([
            mov.data_movimentacao.strftime("%d/%m/%Y"),
            mov.tipo.title(),
            Paragraph(mov.descricao, texto),
            mov.categoria,
            mov.forma_pagamento,
            Paragraph(valor, texto),
        ])

    tabela = Table(
        dados,
        repeatRows=1,
        colWidths=[
            2.3 * cm,
            2.3 * cm,
            6.5 * cm,
            3.2 * cm,
            3.0 * cm,
            2.8 * cm,
        ]
    )

    estilo = TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),

        ("GRID", (0, 0), (-1, -1), 0.30, colors.HexColor("#E5E7EB")),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),

    ])

    for i in range(1, len(dados)):

        if i % 2 == 0:

            estilo.add(
                "BACKGROUND",
                (0, i),
                (-1, i),
                colors.HexColor("#F8FAFC")
            )

    tabela.setStyle(estilo)

    elementos.append(tabela)

    elementos.append(
        Spacer(
            1,
            0.7 * cm
        )
    )

    # ==========================================================
    # RODAPÉ
    # ==========================================================

    elementos.append(
        Paragraph(
            "<font color='#64748B'>Relatório gerado automaticamente pelo GestCar Pro</font>",
            texto
        )
    )

    elementos.append(
        Paragraph(
            datetime.now().strftime("%d/%m/%Y %H:%M"),
            texto
        )
    )

    # ==========================================================
    # FINALIZA PDF
    # ==========================================================

    doc.build(elementos)

    return response