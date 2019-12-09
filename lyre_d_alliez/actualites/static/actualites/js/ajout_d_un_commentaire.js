$(function ()
{
    /* Fonctions */
    /* --------- */

    /* Fonction concernant la requête de soumission d'un commentaire */
    let requete_soumission_commentaire = function()
    {
        let form = $("#formulaire-actualites");

        $.ajax(
        {
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',
            success: function()
            {
                requete_recuperation_commentaires();

                form.each(function()
                {
                    this.reset();
                });
            }
        });
    };

    /* Fonction concernant la requête de récupération des commentaires */
    let requete_recuperation_commentaires = function()
    {
        let button = $(".js-ajout-commentaire");

        $.ajax(
        {
            url: button.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data)
            {
                $("#conteneur_commentaires_article").html(data.html_form);
            },
        });
    };

    /* Fonction concernant l'ajout d'un commentaire et la récupération de la liste des commentaires */
    let ajoutCommentaire = function()
    {
        requete_soumission_commentaire();
    };

    /* Liens */
    /* ----- */

    $(".js-ajout-commentaire").click(ajoutCommentaire);
});
