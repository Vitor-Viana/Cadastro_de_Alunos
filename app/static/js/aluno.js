function excluir_aluno(excluir_aluno, nome_aluno) {
    var valor_logico = window.confirm("Tem certeza que deseja excluir o(a) aluno(a) " + nome_aluno + "!")
    if (valor_logico) 
        window.open(excluir_aluno, "_self");
}