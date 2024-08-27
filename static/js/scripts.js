document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour vérifier si un élément est dans la fenêtre
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Fonction pour envoyer une requête pour incrémenter le compteur
    function incrementConsultation(avisId) {
        fetch('/increment-consultation/' + avisId, {  // URL adaptée à votre route Flask
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')  // Incluez un token CSRF si nécessaire
            },
        })
        .then(response => {
            if (response.ok) {
                console.log('Consultation count incremented');
            } else {
                console.error('Error incrementing consultation count');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }

    // Sélectionner tous les éléments avec la classe 'encadrement2'
    const avisElements = document.querySelectorAll('.encadrement2');
    avisElements.forEach(function(div) {
        // Afficher ou masquer les détails au clic
        div.addEventListener('click', function() {
            const details = this.querySelector('.details');
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
            } else {
                details.style.display = 'none';
            }

            // Envoyer une requête pour enregistrer le clic
            incrementConsultation(this.id.replace('avis', '').replace('_H1', ''));  // Extrait l'ID de l'animal
        });

        // Vérifier si l'élément est dans la fenêtre au chargement
        if (isElementInViewport(div)) {
            incrementConsultation(div.id.replace('avis', '').replace('_H1', ''));  // Extrait l'ID de l'animal
        }
    });

    // Vérifier la visibilité des éléments au défilement
    // window.addEventListener('scroll', function() {
    //     avisElements.forEach(function(div) {
    //         if (isElementInViewport(div)) {
    //             incrementConsultation(div.id.replace('avis', '').replace('_H1', ''));  // Extrait l'ID de l'animal
    //         }
    //     });
    // });
});