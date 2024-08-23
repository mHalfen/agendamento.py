document.addEventListener('DOMContentLoaded', function() {
    const cnpjInput = document.getElementById('cnpj');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', function() {
            const termo = this.value;
            if (termo.length > 1) {
                fetch(`/suggestions?termo=${termo}`)
                    .then(response => response.json())
                    .then(data => {
                        const suggestionsDiv = document.getElementById('cnpj-suggestions');
                        suggestionsDiv.innerHTML = '';
                        data.forEach(suggestion => {
                            const suggestionElement = document.createElement('div');
                            suggestionElement.textContent = `${suggestion.cnpj} - ${suggestion.razao_social}`;
                            suggestionElement.addEventListener('click', function() {
                                document.getElementById('cnpj').value = suggestion.cnpj;
                                document.getElementById('fornecedor').value = suggestion.razao_social;
                                suggestionsDiv.innerHTML = '';
                            });
                            suggestionsDiv.appendChild(suggestionElement);
                        });
                    });
            }
        });
    }
});
