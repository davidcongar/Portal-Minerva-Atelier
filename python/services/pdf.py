
from python.models.modelos import *
import io

import pandas as pd
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image,KeepTogether
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.units import inch
from sqlalchemy.inspection import inspect
import io
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from svglib.svglib import svg2rlg
import os
from python.models import db
from python.services.system.helper_functions import *
from python.services.dynamic_routes_functions import *
from flask import request
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import aliased
from python.services.pdf import *
from datetime import datetime

#####
# funciones de formularios
#####

HANDLERS = {}

def handler_pdf(*tables):
    def wrapper(fn):
        for t in tables:
            HANDLERS[t] = fn
        return fn
    return wrapper

def pdf(table_name, id):
    handler = HANDLERS.get(table_name)
    if not handler:
        logo_path= "./static/images/logo-light.png"
        model = get_model_by_name(table_name)
        # Iniciar la consulta
        query = model.query
        # Agregar joins condicionales
        joins = get_joins()
        filtered_joins = {
            field: val for field, val in joins.items() if field in model.__table__.columns
        }
        for field, (table, id_column, name_column) in filtered_joins.items():
            # Asegura que el campo exista en el modelo base
            if field not in model.__table__.columns:
                continue

            # Crea un alias único por campo (soporta varias uniones al mismo modelo)
            alias = aliased(table, name=f"{table.__tablename__}__{field}")

            # Re-vincula columnas al alias
            alias_id_col = getattr(alias, id_column.key)
            alias_name_col = getattr(alias, name_column.key)

            # Join explícito y ON explícito contra el modelo base
            query = (
                query.outerjoin(alias, alias_id_col == getattr(model, field))
                    .add_columns(alias_name_col.label(f"{field}_{name_column.key}"))
            )
        query=query.filter(model.id == id)
        records = query.all()
        columns_order=get_columns(table_name,'pdf')
        record = [record_to_ordered_list(model,joins,record,columns_order) for record in records]
        record = dict(record[0])
        # 2) Collect relationship data (all rows for each related table)
        parent_model = get_model_by_name(table_name)
        relationships = get_table_relationships(table_name)
        if relationships:
            relationship_table_name=relationships[0]
            related_model = get_model_by_name(relationship_table_name)
            fk_name = None
            for relationships[0], rel in inspect(related_model).relationships.items():
                if rel.mapper.class_ is parent_model:
                    # FK column(s) on the related model
                    local_fk_cols = [c.name for c in rel.local_columns]
                    if local_fk_cols:
                        fk_name = local_fk_cols[0]
                        break
            # Iniciar la consulta
            query = related_model.query
            # Agregar joins condicionales
            joins = get_joins()
            filtered_joins = {
                field: val for field, val in joins.items() if field in related_model.__table__.columns
            }
            for field, (table, id_column, name_column) in filtered_joins.items():
                # Asegura que el campo exista en el modelo base
                if field not in related_model.__table__.columns:
                    continue

                # Crea un alias único por campo (soporta varias uniones al mismo modelo)
                alias = aliased(table, name=f"{table.__tablename__}__{field}")

                # Re-vincula columnas al alias
                alias_id_col = getattr(alias, id_column.key)
                alias_name_col = getattr(alias, name_column.key)

                # Join explícito y ON explícito contra el modelo base
                query = (
                    query.outerjoin(alias, alias_id_col == getattr(related_model, field))
                        .add_columns(alias_name_col.label(f"{field}_{name_column.key}"))
                )
            query=query.filter(getattr(related_model, fk_name) == id)
            related_records = query.all()
            columns_order=get_columns(relationship_table_name,'pdf')
            related_records = [record_to_ordered_list(related_model,joins,record,columns_order) for record in related_records]
            all_related_results = related_records
        # 3) Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="Title", fontSize=16, alignment=TA_CENTER, spaceAfter=8)
        section_title_style = ParagraphStyle(name="SectionTitle", fontSize=13, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6)
        cell_style = ParagraphStyle(name="Cell", fontSize=9, alignment=TA_CENTER, wordWrap='CJK')

        # 4) Document + header callback
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                leftMargin=36, rightMargin=36, topMargin=54, bottomMargin=36)

        def draw_header(canvas, doc_):
            y_top = doc_.height + doc_.topMargin + 10
            y = doc_.height + doc_.topMargin + 10
            if logo_path:
                try:
                    # Draw logo (keep it small and left-aligned)
                    canvas.drawImage(logo_path, doc_.leftMargin, y - 30, width=120, height=30, preserveAspectRatio=True, mask='auto')
                except Exception:
                    pass
            # datetime on the right
            qr_size = 60
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            canvas.setFont("Helvetica", 9)
            x_right = doc_.pagesize[0] - doc_.rightMargin
            canvas.drawRightString(x_right, y_top, now_str)
            canvas.setFont("Helvetica-Bold", 14)
            qr_data = f"{id}"
            # Build the QR widget
            qr_widget = qr.QrCodeWidget(qr_data)
            bounds = qr_widget.getBounds()
            w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
            # Choose the QR size in points (72 points = 1 inch)
            # 1 inch square; change to 96/120 for larger
            # Scale the widget to the target size
            d = Drawing(qr_size, qr_size, transform=[qr_size / w, 0, 0, qr_size / h, 0, 0])
            d.add(qr_widget)
            # Coordenadas top-right
            x = doc_.pagesize[0] - doc_.rightMargin - qr_size
            y_qr = y_top - qr_size
            # Dibuja el QR en el canvas
            renderPDF.draw(d, canvas, x, y_qr)
        # 5) Flowables
        story = []
        # Spacer under header
        story.append(Spacer(1, 40))
        story.append(Paragraph(table_name.replace('_', ' ').capitalize(), title_style))
        story.append(Spacer(1, 20))
        # --- Parent record section ---
        parent_data = [
            [Paragraph(str(k.replace('id_','').replace('_', ' ').capitalize() if k!='id_visualizacion' else 'ID'), cell_style), Paragraph(str(v) if v not in (None, "") else "N/A", cell_style)]
            for k, v in record.items()
        ]
        parent_table = Table(parent_data, repeatRows=1, colWidths=[doc.width * 0.32, doc.width * 0.68])
        parent_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F3F5")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFBFD")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(parent_table)
        # --- Related records sections ---
        if relationships:
            story.append(Spacer(1, 16))
            story.append(Paragraph(relationship_table_name.replace('_', ' ').capitalize(), section_title_style))
            story.append(Spacer(1, 16))

            # Determine column order: all skeys, but drop the FK column (since it's the same for all rows)
            # Build table data
            data = [ [Paragraph(str(k.replace('id_','').replace('_', ' ').capitalize() if k!='id_visualizacion' else 'ID'), cell_style) for k in columns_order] ]
            for row in all_related_results:
                data.append([Paragraph(str(k[1]) if k[1] not in (None, "") else "N/A", cell_style) for k in row])
            # Compute reasonable column widths
            num_cols = 1 + len(columns_order)
            col_widths = [doc.width * 0.08] + [ (doc.width * 0.92) / max(1, len(columns_order)) ] * len(columns_order)

            rel_table = Table(data, repeatRows=1, colWidths=col_widths)
            rel_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F3F5")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE1E6")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFBFD")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))

            # Keep section title + table together when possible
            story.append(KeepTogether([rel_table]))
        # 6) Build PDF
        try:
            doc.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
        except Exception as e:
            import traceback; traceback.print_exc()
            return None, f"Error al construir PDF: {str(e)}"

        buffer.seek(0)
        return buffer.getvalue(), None                                   
    return handler(id)

@handler_pdf('reportes_interacciones')
def pdf_reportes_interacciones(id):
    record=Reportes.query.get(id)

    path = f'./static/sql/report_queries/{record.ruta_sql}.sql'
    base_query = open(path, "r", encoding="utf-8").read()
    df = pd.read_sql(str(base_query), db.engine)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    story = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="RightAlign", parent=styles["Normal"],fontSize=7, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name="CenterHeading5", parent=styles["Heading5"], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="Legend", parent=styles["Normal"],fontSize=7, alignment=TA_LEFT))

    # Draw header function
    def draw_page_decorations(canvas, doc):
        canvas.saveState()

        # --- Page setup ---
        page_width, page_height = landscape(letter)

        # --- Background color ---
        # You can pick any color (hex, RGB, etc.)
        canvas.setFillColor(colors.HexColor("#FAFAFA"))  # light gray background
        canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)

        # --- Header ---
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.black)
        y = page_height - doc.topMargin + 5
        canvas.drawString(doc.leftMargin, y, f"Generado: {pd.Timestamp.now().strftime('%d-%b-%Y')}")

        canvas.restoreState()
    for sector, df_sector in df.groupby("sector"):
        story.append(Paragraph(f"Seguimiento: {sector}", styles["Heading1"]))
        story.append(Spacer(1, 6))

        for region, df_region in df_sector.groupby("region"):
            story.append(Paragraph(f"Resumen de Interacciones Exitosas ({region})", styles["Heading2"]))
            story.append(Spacer(1, 8))

            for categoria, df_cat in df_region.groupby("categoria_cliente"):
                story.append(Paragraph(f"{categoria}", styles["Heading4"]))
                story.append(Spacer(1, 6))

                # 🔹 Build all tipo_interaccion tables first
                tipo_blocks = []
                first_table = True

                for tipo, df_tipo in df_cat.groupby("tipo_interaccion"):
                    # Header for tipo_interaccion
                    tipo_title = Paragraph(f"<b>{tipo[1:len(tipo)]}</b>", styles["CenterHeading5"])
                    if first_table:
                        headers = ["", "UI", "1Q", "2Q", "3Q", "4Q","4W", "3W", "2W", "1W", "Total"]
                    else:
                        headers = ["UI", "1Q", "2Q", "3Q", "4Q","4W", "3W", "2W", "1W", "Total"]
                    table_data = [headers]

                    for _, row in df_tipo.iterrows():
                        if first_table:
                            # Include Cliente only in the first table
                            table_data.append([
                                row["cliente"],
                                row["ultima_interaccion"].strftime("%d-%b") if row["ultima_interaccion"] else "-",
                                int(row["q1"] or 0), int(row["q2"] or 0), int(row["q3"] or 0), int(row["q4"] or 0),
                                int(row["w4"] or 0), int(row["w3"] or 0), int(row["w2"] or 0), int(row["w1"] or 0),
                                int(row["total"] or 0)
                            ])
                        else:
                            # Omit Cliente for subsequent tables
                            table_data.append([
                                row["ultima_interaccion"].strftime("%d-%b") if row["ultima_interaccion"] else "-",
                                int(row["q1"] or 0), int(row["q2"] or 0), int(row["q3"] or 0), int(row["q4"] or 0),
                                int(row["w4"] or 0), int(row["w3"] or 0), int(row["w2"] or 0), int(row["w1"] or 0),
                                int(row["total"] or 0)
                            ])

                    totals = df_tipo[["q1", "q2", "q3", "q4", "w4", "w3", "w2", "w1", "total"]].sum()
                    if first_table:
                        totals_row = [
                            Paragraph("<b>Total</b>", styles["RightAlign"]), "",
                            int(totals.q1), int(totals.q2), int(totals.q3), int(totals.q4),
                            int(totals.w4), int(totals.w3), int(totals.w2), int(totals.w1),
                            int(totals.total)
                        ]
                    else:
                        totals_row = [
                            "",
                            int(totals.q1), int(totals.q2), int(totals.q3), int(totals.q4),
                            int(totals.w4), int(totals.w3), int(totals.w2), int(totals.w1),
                            int(totals.total)
                        ]    
                    table_data.append(totals_row)           
                    if first_table:
                        col_widths = [
                            1*inch,  # Cliente (wider)
                            0.4*inch,  # Última interacción
                            *([0.2*inch]*8),  # Quarters + Weeks
                            0.3*inch   # Total
                        ]
                    else:
                        col_widths = [
                            0.4*inch,  # Última interacción
                            *([0.2*inch]*8),
                            0.3*inch
                        ]
                    t = Table(table_data, repeatRows=1, hAlign='CENTER', colWidths=col_widths)
                    table_style=TableStyle([
                        # --- Header ---
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FAFAFA")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 8),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
                        ("TOPPADDING", (0, 0), (-1, 0), 4),

                        # --- Body ---
                        ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -2), 8),
                        ("ALIGN", (0, 1), (-1, -2), "CENTER"),
                        ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 1), (-1, -1), 2),
                        ("BOTTOMPADDING", (0, 1), (-1, -1), 2),

                        # --- Alternating Row Colors ---
                        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.HexColor("#FAFAFA")]),

                        # --- Totals Row ---
                        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                        ("FONTSIZE", (0, -1), (-1, -1), 8),
                        ("ALIGN", (0, -1), (-1, -1), "CENTER"),
                        ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),

                        # --- Grid / Lines ---
                        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black),     # strong header underline
                        ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#CCCCCC")),  # light dotted lines
                    ])
                    for i, row in enumerate(table_data[1:-1], start=1):  # skip header and last row
                        try:
                            last_interaction_str = row[1]
                            if last_interaction_str == "-" or not last_interaction_str:
                                continue  
                            last_interaction = datetime.strptime(last_interaction_str, "%d-%b")
                            last_interaction = last_interaction.replace(year=datetime.today().year)
                            days_diff = (datetime.today().date() - last_interaction.date()).days
                            if days_diff > 60:
                                color = colors.HexColor("#FFB3B3")  # light red
                            elif days_diff > 30: 
                                color = colors.HexColor("#FFF4B3")  # light yellow
                            else:  
                                color = colors.HexColor("#C6F5C6")  # light green
                            table_style.add("BACKGROUND", (0, i), (0, i), color)
                            table_style.add("TEXTCOLOR", (0, i), (0, i), colors.black)

                        except Exception:
                            continue  # ignore parsing errors
                    t.setStyle(table_style)


                    # Each tipo_interaccion block (title + table)
                    tipo_blocks.append([tipo_title, Spacer(1, 4), t])
                    first_table = False                        
                # 🔹 Arrange tipo_interaccion blocks in a 4-column grid
                page_width, _ = landscape(letter)
                usable_width = page_width - doc.leftMargin - doc.rightMargin
           
                num_cols = 4
                rows = [tipo_blocks[i:i + num_cols] for i in range(0, len(tipo_blocks), num_cols)]

                # Fill incomplete rows with empty cells to keep shape
                for r in rows:
                    while len(r) < num_cols:
                        r.append([])
                colWidths = [
                    usable_width * 0.31,
                    usable_width * 0.23,
                    usable_width * 0.23,
                    usable_width * 0.23
                ]
                grid = Table(rows, colWidths=colWidths)
                grid.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]))

                story.append(grid)
                story.append(Spacer(1, 12))

            legend_data = [
                [
                    Paragraph(
                        "<b>Código de clientes:</b><br/>"
                        "Sin exitosas en más de 2 meses.<br/>"
                        "Sin interacciones exitosas en las últimas 4 semanas.<br/>"
                        "Al menos una exitosa en las últimas 4 semanas.",
                        styles["Legend"]
                    ),
                    "",  # color boxes column
                ]
            ]

            legend = Table(
                legend_data,
                colWidths=[3.0 * inch, 0.25 * inch],
                hAlign="LEFT"
            )

            legend.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TEXTCOLOR", (0, 0), (0, 0), colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("LEADING", (0, 0), (0, 0), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))

            # Add the stacked colored boxes to the right cell
            color_boxes = Table(
                [
                    [""],
                    [""],
                    [""],
                    [""],
                ],
                colWidths=[0.25 * inch],
                rowHeights=[0.15 * inch] * 4,
            )
            color_boxes.setStyle(TableStyle([
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#FFB3B3")),  # red
                ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#FFF4B3")),  # yellow
                ("BACKGROUND", (0, 3), (0, 3), colors.HexColor("#C6F5C6")),  # green
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),                
            ]))

            legend._argW[1] = 0.25 * inch  # ensure fixed width for color column
            legend._cellvalues[0][1] = color_boxes

            story.append(legend)
            story.append(Spacer(1, 6))
            story.append(PageBreak())
    try:
        doc.build(story, onFirstPage=draw_page_decorations, onLaterPages=draw_page_decorations)
    except Exception as e:
        import traceback; traceback.print_exc()
        return None, f"Error al construir PDF: {str(e)}"

    buffer.seek(0)
    return buffer.getvalue(), None    

