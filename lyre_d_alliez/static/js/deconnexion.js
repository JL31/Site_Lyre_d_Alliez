$(function ()
{
    /* Fonctions */
    /* --------- */

    let affichageDeconnexion = function()
    {
        let element = $(this);

        $.ajax(
        {
            url: element.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function ()
            {
                $("#id_panneau_lateral").modal("hide");
                $("#modal-deconnexion").modal("show");
            },
            success: function (data)
            {
                $("#modal-deconnexion .modal-content.deconnexion").html(data.html_content);
            }
        });
    };

    let fermetureDeconnexion = function()
    {
        let form = $(this);

        $.ajax(
        {
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data)
            {
                $("#modal-deconnexion").modal("hide");
                window.location.replace(data.url_pour_redirection);
            }
        });

        return false;
    };

    /* Liens */
    /* ----- */

    $("#lien_deconnexion").click(affichageDeconnexion);
    $("#modal-deconnexion").on("submit", ".js-ok-deconnexion", fermetureDeconnexion);
});
