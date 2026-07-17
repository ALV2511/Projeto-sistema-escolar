// Executa assim que a página carrega
document.addEventListener("DOMContentLoaded", () => {
    listarAlunos();

    // Monitora o envio do formulário de cadastro
    document.getElementById("form-cadastro").addEventListener("submit", cadastrarAluno);
});

// Função para buscar e renderizar os alunos do Excel
async function listarAlunos() {
    const resposta = await fetch("/api/alunos");
    const alunos = await resposta.json();
    
    const tbody = document.getElementById("tabela-alunos");
    tbody.innerHTML = ""; // Limpa a tabela antes de preencher

    alunos.forEach(aluno => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${aluno.ID}</td>
            <td>${aluno.Nome}</td>
            <td>${aluno.Média.toFixed(2)}</td>
            <td style="font-weight: bold; color: ${aluno.Status === 'Aprovado' ? 'green' : 'red'}">${aluno.Status}</td>
            <td>
                <button class="btn-excluir" onclick="excluirAluno(${aluno.ID})">Excluir</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Função para cadastrar o aluno
async function cadastrarAluno(event) {
    event.preventDefault(); // Evita que a página recarregue

    const nome = document.getElementById("nome").value;
    const nota1 = parseFloat(document.getElementById("nota1").value);
    const nota2 = parseFloat(document.getElementById("nota2").value);

    const resposta = await fetch("/api/alunos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ nome, nota1, nota2 })
    });

    if (resposta.ok) {
        document.getElementById("form-cadastro").reset(); // Limpa os campos
        listarAlunos(); // Atualiza a tabela na tela
    } else {
        alert("Erro ao cadastrar aluno.");
    }
}

// Função para deletar um aluno
async function excluirAluno(id) {
    if (confirm(`Deseja mesmo excluir o aluno com ID ${id}?`)) {
        const resposta = await fetch(`/api/alunos/${id}`, {
            method: "DELETE"
        });

        if (resposta.ok) {
            listarAlunos(); // Atualiza a tabela
        } else {
            alert("Erro ao excluir aluno.");
        }
    }
}