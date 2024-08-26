document.addEventListener("DOMContentLoaded", function() {
    // Sélectionner tous les éléments avec la classe 'encadrement2'
    document.querySelectorAll('.encadrement2').forEach(function(div) {
        div.addEventListener('click', function() {
            // Afficher ou masquer les détails
            const details = this.querySelector('.details');
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
            } else {
                details.style.display = 'none';
            }

            // Envoyer une requête pour enregistrer le clic
            fetch('/update-vet-record', {  // Ajustez l'URL en fonction de votre route Flask
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ avisId: this.id })  // Assurez-vous que 'avisId' est la clé correcte
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Clic enregistré avec succès');
                } else {
                    console.error('Erreur lors de l\'enregistrement du clic');
                }
            })
            .catch(error => {
                console.error('Erreur réseau :', error);
            });
        });
    });
});


/*!
* Start Bootstrap - Business Casual v7.0.9 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
// Highlights current date on contact page
// window.addEventListener('DOMContentLoaded', event => {
//     const listHoursArray = document.body.querySelectorAll('.list-hours li');
//     listHoursArray[new Date().getDay()].classList.add(('today'));
// })

// document.querySelectorAll('.encadrement2').forEach(function(div) {
//     div.addEventListener('click', function() {
//         const details = this.querySelector('.details');
//         if (details.style.display === 'none' || details.style.display === '') {
//             details.style.display = 'block';
//         } else {
//             details.style.display = 'none';
//         }

//         // Envoyer une requête pour enregistrer le clic
//         fetch('https://votre-serveur.com/enregistrer-clic', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ avisId: this.id })
//         }).then(response => {
//             if (!response.ok) {
//                 console.error('Erreur lors de l\'enregistrement du clic');
//             }
//         }).catch(error => {
//             console.error('Erreur réseau :', error);
//         });
//     });
// });

// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelectorAll('.encadrement2').forEach(function(encadrement) {
//         encadrement.addEventListener('click', function() {
//             const animalId = this.dataset.animalId;
            
//             fetch('/admin', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded'
//                 },
//                 body: new URLSearchParams({
//                     'animal_id': animalId
//                 })
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     console.log('Consultation recorded successfully.');
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//         });
//     });
// });