#!/usr/bin/env bash
# Compila la memoria y el documento de cambios, y monta entrega/E1_REP_BDII4_RENFE.zip
# Uso (desde la raíz del repo): ./scripts/empaquetar_entrega.sh
# Requiere latexmk + pdflatex. Si no los tenéis, compilad en Overleaf y copiad los
# PDF a entrega/ con los nombres E1_REP_BDII4_RENFE_MEM.pdf y E1_REP_BDII4_RENFE_CAM.pdf.
set -euo pipefail
cd "$(dirname "$0")/.."
( cd memoria && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex )
( cd cambios && latexmk -pdf -interaction=nonstopmode -halt-on-error cambios.tex )
cp memoria/main.pdf     entrega/E1_REP_BDII4_RENFE_MEM.pdf
cp cambios/cambios.pdf  entrega/E1_REP_BDII4_RENFE_CAM.pdf
cp sql/E1_REP_BDII4_RENFE_SQL.sql entrega/
rm -f entrega/E1_REP_BDII4_RENFE.zip
( cd entrega && zip -j E1_REP_BDII4_RENFE.zip E1_REP_BDII4_RENFE_MEM.pdf E1_REP_BDII4_RENFE_SQL.sql E1_REP_BDII4_RENFE_CAM.pdf )
echo "Listo: entrega/E1_REP_BDII4_RENFE.zip"
unzip -l entrega/E1_REP_BDII4_RENFE.zip
