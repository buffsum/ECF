/*!
* Start Bootstrap - Business Casual v7.0.9 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
// Highlights current date on contact page
window.addEventListener('DOMContentLoaded', event => {
    const listHoursArray = document.body.querySelectorAll('.list-hours li');
    listHoursArray[new Date().getDay()].classList.add(('today'));
})

document.querySelectorAll('.encadrement2').forEach(function(div) {
    div.addEventListener('click', function() {
        const details = this.querySelector('.details');
        if (details.style.display === 'none' || details.style.display === '') {
            details.style.display = 'block';
        } else {
            details.style.display = 'none';
        }

        // Envoyer une requête pour enregistrer le clic
        fetch('https://votre-serveur.com/enregistrer-clic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ avisId: this.id })
        }).then(response => {
            if (!response.ok) {
                console.error('Erreur lors de l\'enregistrement du clic');
            }
        }).catch(error => {
            console.error('Erreur réseau :', error);
        });
    });
});