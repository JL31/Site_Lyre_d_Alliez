$(function ()
{
    /* Fonctions */
    /* --------- */

    let chargementFormulaireAbonnementEvenement = function()
    {
        let btn = $(this);

        $.ajax(
        {
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function ()
            {
                $("#modal-abonnement-evenement").modal("show");
            },
            success: function (data)
            {
                $("#modal-abonnement-evenement .modal-content").html(data.html_form);
            }
        });
    };

    let sauvegardeFormulaireAbonnementEvenement = function()
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
                if (data.form_is_valid)
                {
                    alert("Abonnement terminé !");
                    $("#modal-abonnement-evenement").modal("hide");
                }
                else
                {
                    $("#modal-abonnement-evenement .modal-content").html(data.html_form);
                }
            }
        });

        return false;

    };

    /* Liens */
    /* ----- */

    $(".js-abonnement-evenement").click(chargementFormulaireAbonnementEvenement);
    $("#modal-abonnement-evenement").on("submit", ".js-abonnement-evenement-creation-formulaire", sauvegardeFormulaireAbonnementEvenement);

});
