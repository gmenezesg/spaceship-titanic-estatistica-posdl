import nbformat
from nbclient import NotebookClient
import pytest
from pathlib import Path

def test_notebook_kan28_execution_and_summary_table():
    notebook_path = Path("notebooks/04_testes_hipoteses_anova.ipynb")
    assert notebook_path.exists(), "Notebook 04_testes_hipoteses_anova.ipynb não encontrado"
    
    nb = nbformat.read(notebook_path, as_version=4)
    assert len(nb.cells) >= 31, f"Esperado pelo menos 31 células, encontrado {len(nb.cells)}"
    
    client = NotebookClient(nb, timeout=240, kernel_name="python3")
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
    
    # Validações estruturais da KAN-28
    assert "KAN-28: Tabela-Resumo Consolidada dos Testes de Hipóteses" in full_text
    assert "10 linhas x 9 colunas" in full_text
    
    # Validações das 9 colunas normativas
    assert "Pergunta de Pesquisa / Relação Analisada" in full_text
    assert "Hipótese Nula (H0) e Alternativa (H1)" in full_text
    assert "Teste Estatístico Aplicado" in full_text
    assert "Verificação dos Pressupostos" in full_text
    assert "Valor da Estatística do Teste" in full_text
    assert "Valor-p Observado" in full_text
    assert "Tamanho do Efeito" in full_text
    assert "Decisão Estatística (alpha=0.05)" in full_text
    assert "Conclusão em Lógica de Negócio" in full_text
    
    # Validações dos testes consolidados na tabela
    assert "338.82" in full_text  # chi2 HomePlanet
    assert "1897.71" in full_text  # chi2 CryoSleep
    assert "12.07" in full_text  # chi2 VIP
    assert "0.467" in full_text  # Cramer V CryoSleep
    assert "18.94" in full_text  # t Welch
    assert "0.407" in full_text  # d Cohen
    assert "407.57" in full_text  # F Welch
    assert "0.1714" in full_text  # eta^2
    assert "271.97" in full_text  # H Kruskal-Wallis
    assert "2768.76" in full_text  # Games-Howell Europa vs Earth
    assert "--- KAN-28: Tabela Exportada em Formato Markdown ---" in full_text

if __name__ == "__main__":
    test_notebook_kan28_execution_and_summary_table()
    print("Todas as asserções da KAN-28 passaram com sucesso!")
