var Charace = Charace || {};

Charace.Config = {
    spriteSize: 120
};

Charace.Racetrack = function () {

    var $racetrack = undefined;
    var racetrackWhitespaceHeight = undefined;
    var racetrackWidth = undefined;

    var selectedLinkUrl = undefined;
    var charities = {};
    var goal = 200000;

    var setGoal = function (g) { goal = g; };
    var getGoal = function () { return goal; };

    var initialise = function () {
        $racetrack = $("#racetrack");
        updateSizes();
        getCharities();
        window.setInterval(getCharityPoints, 5000);
    };

    var getCharities = function () {
        $.get("/api/getCharities", function (data) {
            for (var charityId in data){
                charities[charityId] = {};
                charities[charityId].name = data[charityId];
                charities[charityId].points = 0;
                charities[charityId].update = false;
                $racetrack.append('<div class="charity" data-charity="' + charityId + '"></div>');
                $racetrack.append('<div class="charity-name" data-charity="' + charityId + '">' + charities[charityId].name + '</div>')
            }
            render();
            getCharityPoints();
            createDonate();
        });
    };

    var getCharityPoints = function () {
        $.get("/api/getPoints", function (data) {
            for (var charityId in data) {
                if (data[charityId] != charities[charityId].points) {
                    charities[charityId].points = data[charityId];
                    charities[charityId].update = true;
                }
            }
            render();
        })
    };

    var updateSizes = function () {
        racetrackWhitespaceHeight = ($racetrack.height() - 4*Charace.Config.spriteSize)/3;
        racetrackWidth = $racetrack.width() - Charace.Config.spriteSize;
    };

    var render = function () {
        var i = 0;
        for (var charityId in charities) {
            var charity = charities[charityId];
            if (charity.update) {
                var charityEl = $('.charity[data-charity="' + charityId + '"]');
                var charityNameEl = $('.charity-name[data-charity="' + charityId + '"]');
                charityEl.css("top", (racetrackWhitespaceHeight + Charace.Config.spriteSize) * i + "px");
                charityEl.css('background-image','url(/static/Gifs/' + charityId + '_Moving.gif');
                (function (charityId, charityEl) {
                    charityEl.animate({
                        "left": (charity.points / goal) * racetrackWidth + "px"
                    }, 2000, function () {
                         charityEl.css('background-image','url(/static/Gifs/' + charityId + '_Idle.gif');
                    });
                })(charityId, charityEl);
                charityNameEl.css("top", (racetrackWhitespaceHeight + Charace.Config.spriteSize) * i + "px");
                charityNameEl.animate({
                    "left": (charity.points/ goal) * racetrackWidth + (charity.points/goal < 0.5 ? 80 : - 10 - charityNameEl.width()) + "px"
                }, 2000);
            }
            charity.update = false;
            i++;
        }
    };

    var createDonate = function () {
        $('#donate-window').show(1000);
        $select = $('#donate-select');
        for (var charityId in charities) {
            var charity = charities[charityId];
            $select.append('<option value="' + charityId + '">' + charity.name + '</option>');
        }
        $select.change(function () {
            changeDonateButton($('#donate-select option:selected').val());
        });
        $('#donate-button').click(function () {
            if (selectedLinkUrl != undefined) {
                window.open(selectedLinkUrl);
            }
        })
    };

    var changeDonateButton = function (charityId) {
        $donateFields = $('.donate-fields');
        if (charityId == "undefined") return;
        $.get("/api/post/" + charityId, function (data) {
            $('#donate-description').text(data.description);
            selectedLinkUrl = data.url;
            if (selectedLinkUrl != undefined) {
                $donateFields.show();
            }else {
                $donateFields.hide();
            }
        });
    };

    return {
        setGoal: setGoal,
        getGoal: getGoal,
        initialise: initialise,
        render: render,
    };
}();

$(document).ready(function (){
   Charace.Racetrack.initialise();
});