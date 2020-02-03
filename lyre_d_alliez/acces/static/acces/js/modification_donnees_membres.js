$(function ()
{
    /* Fonctions */
    /* --------- */

    let retourAccueil = function()
    {
        let btn = $(this);
        let url_pour_redirection = btn.attr("url_pour_redirection");

        window.location.replace(url_pour_redirection);
    };

    /* Liens */
    /* ----- */

    $("#bouton_retour_consultation_modification_donnees_personnelles").click(retourAccueil);
    $("#bouton_annuler_changement_mot_de_passe").click(retourAccueil);
    $("#bouton_annuler_suppression_du_compte").click(retourAccueil);
});
