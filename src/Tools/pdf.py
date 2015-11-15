# -*- coding: utf-8 -*-
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer, TableStyle, Image
from reportlab.pdfbase.pdfmetrics import stringWidth

from Tools.timeFunctions import todaysDate, int2date
import config.GlobalConstants as Constants


class PDFmethods():
	def __init__(self):
		self.cols = 2
		self.lbreak = 10
		self.vdelay = 0

	def Y(self, y, unit=mm):
		return self.height - (y + self.vdelay) * unit

	def X(self, x, unit=mm):
		return x * unit

	def coord(self, x, y, unit=mm):
		"""
		# http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
		Helper class to help position flowables in Canvas objects
		"""
		return self.X(x), self.Y(y)

	def createBarCodes(self, barcode_value, barHeight=23, barWidth=1.2):
		return code128.Code128(barcode_value, barHeight=barHeight, barWidth=barWidth)

	def writeBarcode(self, text, x, y, filePDF):
		self.createBarCodes(text).drawOn(filePDF, x, y)
		filePDF.drawString(x + 10 * mm, y - 4 * mm, 'ID: %s' % (text, ))

	def cutCross(self, x0, y0):
		y0 -= 5 * mm
		x0 -= 5 * mm
		cross = [
			(x0 - 10, y0, x0 - 5, y0),
			(x0 + 5, y0, x0 + 10, y0),
			(x0, y0 - 10, x0, y0 - 5),
			(x0, y0 + 5, x0, y0 + 10)
		]
		return cross

	def CreateOutput(self, output):
		return canvas.Canvas(output, pagesize=letter)

	def writetext(self, filePDF, font, size, x, y, string):
		filePDF.setFont(font, size)
		filePDF.drawString(x, y, string)

	def rectangle(self, x0, y0, x1, y1):
		return [
			(x0, y0, x1, y0),  # horizontal down
			(x0, y1, x1, y1),  # horizontal top
			(x0, y0, x0, y1),  # horizontal left
			(x1, y0, x1, y1),  # horizontal right
		]

	def writeTitle(self, target, text, font, size):
		textWidth = stringWidth(text, font, size)
		self.writetext(target, font, size, (self.width - textWidth) / 2, self.Y(5), text)

	def writeSubTitle(self, target, text, font, size):
		textWidth = stringWidth(text, font, size)
		self.writetext(target, font, size, (self.width - textWidth) / 2, self.Y(15), text)

	def writeTableTitle(self, target, text, font, size, y):
		textWidth = stringWidth(text, font, size)
		self.writetext(target, font, size, (self.width - textWidth) / 2, y, text)

	def writeDate(self, target, text, font, size):
		textWidth = stringWidth(text, font, size)
		self.writetext(target, font, size, self.width - 1.5 * textWidth, self.Y(0), text)

	def writeHeaders(self, target, headers, x0, y0, dy, font, size):
		for i in range(0, len(headers)):
			text = headers[i]
			self.writetext(target, font, size, x0, self.Y(35) - i * dy, text)

	def writeHeadersValue(self, target, headers, x0, y0, dy, font, size):
		for i in range(0, len(headers)):
			text = headers[i]
			self.writetext(target, font, size, x0, self.Y(35) - i * dy, ":  " + text)

	def drawLogo(self, target, logo, x, y):
		# #####		  Logo
		logo = Image(logo)
		logo.drawHeight = 1 * inch
		logo.drawWidth = 1 * inch
		logo.drawOn(target, * self.coord(x, y))


class DefaultReport(PDFmethods):
	def __init__(self, data, output, colWidths, title='title', subtitle='subtitle', orientation=Constants.PAPER_PORTAIL, parent=None):
		if orientation == Constants.PAPER_LANDSCAPE:
			self.width, self.height = landscape(letter)
		else:
			self.width, self.height = letter

		self.vdelay = 20
		self.data = data
		if len(colWidths) > 1:
			self.colWidths = self.colsize(colWidths)
		else:
			self.colWidths = colWidths[0]
		self.oFile = output
		self.title = title
		self.subtitle = subtitle
		self.run()

	def colsize(self, colWidths):
		'''
		Normalizes the column width in order to use the complete width of the page
		'''
		totWidth = 0
		for i in range(0, len(colWidths)):
			totWidth += colWidths[i]
		delta = max(self.width - totWidth - 15 * mm, 0)

		for i in range(0, len(colWidths)):
			colWidths[i] = colWidths[i] * (1 + delta / totWidth)
		return colWidths

	def run(self):
		self.doc = SimpleDocTemplate(self.oFile, pagesize=(self.width, self.height), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
		self.elements = [Spacer(1, 2 * inch)]
		self.maketable(self.data)
		self.fillTable()
		self.doc.build(self.elements, onFirstPage=self.createDocument)

	def fillTable(self):
		self.style = TableStyle(
			[
				('ALIGN', (1, 1), (1, -1), 'LEFT'),
				('ALIGN', (0, 0), (-1, 0), 'CENTER'),
				('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
				('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
				('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
				('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
				('BOX', (0, 0), (-1, -1), 0.25, colors.black),
			]
		)

		# Configure style and word wrap
		self.s = getSampleStyleSheet()
		self.s = self.s["BodyText"]
		self.s.wordWrap = 'CJK'
		self.data2 = [[Paragraph(unicode(cell), self.s) for cell in row] for row in self.data]

		self.t = Table(self.data2, self.colWidths)
		self.t.setStyle(self.style)

		# Send the data and build the file
		self.elements.append(self.t)

	def maketable(self, data):
		self.data = []
		for i in range(0, len(data)):
			self.data.append(data[i])

	def createDocument(self, filePDF, doc):
		# font_small = 8
		font_normal = 12
		font_big = 18
		font = 'Helvetica'

		subtitle = self.subtitle
		title = self.title

		self.drawLogo(filePDF, 'images/logo/logo.png', 10, 15)
		self.writeTitle(filePDF, title, font, font_big)
		self.writeTableTitle(filePDF, subtitle, font, font_big, self.Y(35))
		self.writeDate(filePDF, str(int2date(todaysDate())), font, font_normal)

if __name__ == "__main__":
	pass
