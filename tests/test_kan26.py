import nbformat
from nbclient import NotebookClient
import pytest
from pathlib import Path

def test_notebook_kan26_execution_and_statistics():
    notebook_path = Path("notebooks/04_testes_hipoteses_anova.ipynb")
    assert notebook_path.exists(), "Notebook 04_testes_hipoteses_anova.ipynb não encontrado"
    
    nb = nbformat.read(notebook_path, as_version=4)
    assert len(nb.cells) >= 22, f"Esperado pelo menos 22 células, encontrado {len(nb.cells)}"
    
    client = NotebookClient(nb, timeout=120, kernel_name="python3")
    client.execute()
    
    # Salvar notebook executado com todos os outputs
    nbformat.write(nb, notebook_path)
    
    # Coletar todo o texto das saídas de stream
    outputs_text = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            for output in cell.outputs:
                assert output.output_type != "error", f"Erro encontrado em célula: {output.get('evalue')}"
                if output.output_type == "stream":
                    outputs_text.append(output.get("text", ""))
    
    full_text = "\n".join(outputs_text)
    
    # Validações estruturais e estatísticas de KAN-26
    assert "Levene (Brown-Forsythe)" in full_text
    assert "Teste t de Welch" in full_text
    assert "Mann-Whitney U" in full_text
    assert "d de Cohen" in full_text
    assert "r de Rosenthal" in full_text
    
    # Verificar valores numéricos exatos de KAN-26
    assert "18.94" in full_text, "Estatística t de Welch esperada em 18.94"
    assert "131.36" in full_text, "Estatística W de Levene esperada em 131.36"
    assert "13,846,862" in full_text, "Estatística U de Mann-Whitney esperada em 13.846.862"
    assert "1120.74" in full_text, "Diferença de médias esperada em $1120.74"
    assert "0.407" in full_text, "d de Cohen esperado em 0.407"
    assert "0.404" in full_text, "r de Rosenthal esperado em 0.404"
    assert "1004.76" in full_text and "1236.71" in full_text, "Intervalo de confiança esperado em [$1004.76, $1236.71]"

if __name__ == "__main__":
    test_notebook_kan26_execution_and_statistics()
    print("Todas as asserções numéricas e estruturais passaram com sucesso!")
