document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/produits')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#produits tbody');
            tbody.innerHTML = '';
            data.forEach(produit => {
                const row = `
                    <tr>
                        <td>${produit.nom}</td>
                        <td>${produit.prix.toFixed(2)}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Erreur chargement produits:', error);
        });
});
