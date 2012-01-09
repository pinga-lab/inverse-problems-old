NAME=apostila
VERSION=1.0.1
OUTPUT=${NAME}-v${VERSION}.pdf

${OUTPUT}: ${NAME}.tex ${NAME}.bib latex/*.tex figs/*.pdf
	pdflatex ${NAME}
	bibtex ${NAME}
	pdflatex ${NAME}
	pdflatex ${NAME}
	mv ${NAME}.pdf ${OUTPUT}

clean:
	rm ${OUTPUT} ${NAME}.log ${NAME}.toc ${NAME}.aux ${NAME}.out ${NAME}.blg ${NAME}.bbl 
