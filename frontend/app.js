// app.js (Responsável por conectar o JSON ao HTML)

// Função assíncrona para lidar com a leitura do arquivo
async function carregarDadosDRE() {
    try {
        // 1. LER O ARQUIVO JSON usando fetch()
        // O caminho '../data/dre_resultado.json' sobe uma pasta (de frontend) e entra em 'data'.
        const resposta = await fetch('../data/dre_resultado.json'); 
        
        // Trata erro se o arquivo não for encontrado (ex: 404)
        if (!resposta.ok) {
            throw new Error(`Erro ao buscar o JSON: ${resposta.status}`);
        }
        
        // Converte a resposta lida para um objeto JavaScript
        const dadosDRE = await resposta.json();

        // 2. FUNÇÃO AUXILIAR PARA FORMATAR VALORES COMO REAIS (R$)
        const formatarMoeda = (valor) => {
            // Usa o Intl.NumberFormat para formatação monetária segura
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL',
            }).format(valor);
        };

        // 3. INJETAR OS VALORES NO HTML (Manipulação do DOM)
        document.getElementById('receita-bruta').textContent = formatarMoeda(dadosDRE.ReceitaBruta);
        document.getElementById('custos-despesas').textContent = formatarMoeda(dadosDRE.CustosDespesas);
        document.getElementById('lucro-bruto').textContent = formatarMoeda(dadosDRE.LucroBruto);
        
        // Dica de UX: Se o lucro for negativo, pinta de vermelho (usando sua variável de acento)
        if (dadosDRE.LucroBruto < 0) {
            document.getElementById('lucro-bruto').style.color = 'var(--color-accent)'; 
        }
        
    } catch (erro) {
        console.error("Erro ao carregar ou processar os dados da DRE:", erro);
        // Garante que o usuário veja uma mensagem de erro na tela
        document.getElementById('lucro-bruto').textContent = "ERRO: Dados indisponíveis"; 
    }
}

// Chamar a função principal quando a página estiver totalmente carregada
document.addEventListener('DOMContentLoaded', carregarDadosDRE); 

