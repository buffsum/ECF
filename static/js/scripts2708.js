document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.encadrement2').forEach(function(div) {
        div.addEventListener('click', function() {
            console.log('Element clicked:', this.id);

            const details = this.querySelector('.details');
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
            } else {
                details.style.display = 'none';
            }

            // Extraire l'ID de l'élément cliqué pour la soumission du formulaire
            const avisId = this.id.replace('avis', '').replace('_H1', '');
            const form = document.querySelector(`#incrementForm_${avisId}`);

            if (form) {
                // Soumettre le formulaire automatiquement si nécessaire
                form.submit();
            } else {
                console.error('Form not found for avisId:', avisId);
            }
        });
    });
});
