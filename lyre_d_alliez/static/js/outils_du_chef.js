$(function ()
{
    /* Fonctions */
    /* --------- */

    let chargementFormulaireOutilDuChef = function()
    {
        let btn = $(this);

        $.ajax(
        {
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function ()
            {
                $("#modal-outils-du-chef").modal("show");
            },
            success: function (data)
            {
                $("#modal-outils-du-chef .modal-content").html(data.html_form);
            }
        });
    };

    let sauvegardeFormulaireOutilDuChef = function()
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
                    alert("Terminé !");
                    $("#modal-outils-du-chef").modal("hide");
                }
                else
                {
                    $("#modal-outils-du-chef .modal-content").html(data.html_form);
                }
            }
        });

        return false;

    };

    /* Liens */
    /* ----- */

    $(".js-creation-evenement").click(chargementFormulaireOutilDuChef);
    $(".js-creation-article").click(chargementFormulaireOutilDuChef);
    $(".js-creation-article-de-presse").click(chargementFormulaireOutilDuChef);
    $(".js-creation-soutien").click(chargementFormulaireOutilDuChef);
    $(".js-ajouter-photos").click(chargementFormulaireOutilDuChef);
    $(".js-ajouter-videos").click(chargementFormulaireOutilDuChef);

    $("#modal-outils-du-chef").on("submit", ".js-creation-evenement-creation-formulaire", sauvegardeFormulaireOutilDuChef);
    $("#modal-outils-du-chef").on("submit", ".js-creation-article-creation-formulaire", sauvegardeFormulaireOutilDuChef);
    $("#modal-outils-du-chef").on("submit", ".js-creation-article-de-presse-creation-formulaire", sauvegardeFormulaireOutilDuChef);
    $("#modal-outils-du-chef").on("submit", ".js-creation-soutien-creation-formulaire", sauvegardeFormulaireOutilDuChef);
    $("#modal-outils-du-chef").on("submit", ".js-ajouter-photos-creation-formulaire", sauvegardeFormulaireOutilDuChef);
    $("#modal-outils-du-chef").on("submit", ".js-ajouter-videos-creation-formulaire", sauvegardeFormulaireOutilDuChef);
});
