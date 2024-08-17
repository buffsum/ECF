import Formulaire from './formulaire.js';

//on crée le formulaire

export const formulaire = new Formulaire("formulaire");
console.log("test console");
formulaire.maskChamp('societe');

formulaire.maskChamp('email');

//addEventListener pour changer le comportement en fonction du radio coché

formulaire.getElement('particulier').addEventListener('change', () => {formulaire.hideChamp('societe')});

formulaire.getElement('professionnel').addEventListener('change', () => {formulaire.showChamp('societe')});

//adEventListener pour changer le comportement en fonction de l'objet

formulaire.getElement('objet').addEventListener('change', ()  => {formulaire.isSelected('objet', "demande_de_contact", () => formulaire.showChamp('email'), () => formulaire.hideChamp('email'));});

//addEventListener pour récupérer les données du formulaire

formulaire.formulaireHtml.addEventListener('submit',
    (event) => {
        event.preventDefault();
        formulaire.affAnswers();
        console.log(formulaire.answers)
    }
);