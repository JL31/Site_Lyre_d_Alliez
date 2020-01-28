$(function ()
{
    /* Fonctions */
    /* --------- */

    /* Fonction concernant l'affichage du programme d'un évènement via une requête de récupération de ce programme */
    let requete_recuperation_programme_evenement = function()
    {
        let btn = $(this);

        $.ajax(
        {
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function ()
            {
                $("#modal-afficher-programme-evenement").modal("show");
            },
            success: function (data)
            {
                $("#modal-afficher-programme-evenement .modal-content").html(data.html_form);
            }
        });
    };

    /* Liens */
    /* ----- */

    $(".js-affichage-programme-evenement").click(requete_recuperation_programme_evenement);
});
