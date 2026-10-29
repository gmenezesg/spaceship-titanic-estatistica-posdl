import nbformat
from nbclient import NotebookClient
import pytest
from pathlib import Path

def test_notebook_kan27_execution_and_statistics():
    notebook_path = Path("notebooks/04_testes_hipoteses_anova.ipynb")
    assert notebook_path.exists(), "Notebook 04_testes_hipoteses_anova.ipynb não encontrado"
    
    nb = nbformat.read(notebook_path, as_version=4)
    assert len(nb.cells) >= 28, f"Esperado pelo menos 28 células, encontrado {len(nb.cells)}"
    
    client = NotebookClient(nb, timeout=180, kernel_name="python3")
    client.execute()
    
    # Salvar notebook executado com todos os outputs pré-renderizados
    nbformat.write(nb, notebook_path)
    
    # Coletar todo o texto das saídas de stream e display_data/execute_result
    outputs_text = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            for output in cell.outputs:
                assert output.output_type != "error", f"Erro encontrado em célula: {output.get('evalue')} - {output.get('traceback')}"
                if output.output_type == "stream":
                    outputs_text.append(output.get("text", ""))
                elif output.output_type in ("execute_result", "display_data"):
                    data = output.get("data", {})
                    if "text/plain" in data:
                        outputs_text.append(data["text/plain"])
    
    full_text = "\n".join(outputs_text)
    
    # Validações estruturais e conceituais da KAN-27
    assert "ANOVA de Welch" in full_text
    assert "Kruskal-Wallis" in full_text
    assert "Games-Howell" in full_text
    assert "Teste de Dunn" in full_text or "Dunn com Correção de Bonferroni" in full_text
    assert "eta^2" in full_text or "Eta ao Quadrado" in full_text
    
    # Validações numéricas exatas da KAN-27
    assert "1592.08" in full_text, "Estatística W de Levene esperada em 1592.08"
    assert "407.57" in full_text, "Estatística F de Welch esperada em 407.57"
    assert "271.97" in full_text, "Estatística H de Kruskal-Wallis esperada em 271.97"
    assert "0.1714" in full_text, "Eta ao quadrado esperado em 0.1714"
    assert "2768.76" in full_text, "Diferença absoluta Earth vs Europa esperada em 2768.76"
    assert "2384.27" in full_text, "Diferença absoluta Europa vs Mars esperada em 2384.27"
    assert "384.49" in full_text, "Diferença absoluta Earth vs Mars esperada em 384.49"

if __name__ == "__main__":
    test_notebook_kan27_execution_and_statistics()
    print("Todas as asserções numéricas e estruturais da KAN-27 passaram com sucesso!")
