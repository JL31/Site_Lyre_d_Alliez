$(function ()
{
    /* Fonctions */
    /* --------- */

    /* Fonction pour le retour à l'accueil du site */
    let retourAccueil = function()
    {
        let btn = $(this);
        let url_pour_redirection = btn.attr("url_pour_redirection");
        window.location.replace(url_pour_redirection);
    };

    /* Fonction pour l'affichage du formulaire permettant de modifier les données personnelles du membre connecté */
    let affichageFormulaireModificationDonneesPersonnelles = function()
    {
        let btn = $(this);

        $.ajax(
        {
            url: btn.attr("data-url"),
            type: "get",
            dataType: "json",
            beforeSend: function ()
            {
                $("#modal-modification").modal("show");
            },
            success: function (donnees)
            {
                $("#modal-modification .modal-content").html(donnees.html_form);
            }
        });
    };

    /* Fonction pour l'enregistrement des modifications des données personnelles du membre connecté */
    let enregistrementModificationDonneesPersonnelles = function ()
    {
        let form = $(this);

        $.ajax(
        {
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (donnees)
            {
                if (donnees.formulaire_valide)
                {
                    $("#modal-modification").modal("hide");
                    let url_retour_donnees = form.attr("data-url");
                    window.location.replace(url_retour_donnees);
                }
                else
                {
                    $("#modal-modification .modal-content").html(donnees.html_form);
                }
            }
        });

        return false;

    };

    /* Liens */
    /* ----- */

    $("#bouton_retour_consultation_modification_donnees_personnelles").click(retourAccueil);
    $("#bouton_annuler_changement_mot_de_passe").click(retourAccueil);
    $("#bouton_annuler_suppression_du_compte").click(retourAccueil);

    $("#bouton_modification_donnees_personnelles").click(affichageFormulaireModificationDonneesPersonnelles);
    $("#modal-modification").on("submit", ".js-modification-donnees-personnelles-form", enregistrementModificationDonneesPersonnelles );
});
