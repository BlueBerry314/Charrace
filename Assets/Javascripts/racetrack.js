var Charace = Charace || {};

Charace.Config = {
    spriteSize: 80
};

Charace.Racetrack = function () {

    var $racetrack = undefined;
    var racetrackWhitespaceHeight = undefined;
    var racetrackWidth = undefined;


    var charities =
        {
        "1": {"name":"Charity 1", "points":60},
        "2": {"name":"Charity 2", "points":20},
        "3": {"name":"Charity 3", "points":80},
        "4": {"name":"Charity 4", "points":99}
        };
    var goal = 100;

    var setGoal = function (g) { goal = g; };
    var getGoal = function () { return goal; };

    var initialise = function () {
        $racetrack = $("#racetrack");
        updateSizes();
        render();
    };

    var updateSizes = function () {
        racetrackWhitespaceHeight = ($racetrack.height() - 4*Charace.Config.spriteSize)/3;
        racetrackWidth = $racetrack.width() - Charace.Config.spriteSize;
    };

    var render = function () {
        var i = 0;
        for (var charityId in charities) {
            var charity = charities[charityId];
            var charityEl = $('.charity[data-charity="' + charityId + '"]');
            charityEl.css("top",(racetrackWhitespaceHeight + Charace.Config.spriteSize)*i + "px");
            charityEl.animate({
                "left": (charity.points/goal)*racetrackWidth + "px"
            }, 2000, function () {});
            i++;
        }
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