
$(document).ready(function() {

  var food_dict = {};

  //绑定桌布图标的点击事件
  $(".mk_board").delegate(".thumb", "click", function () {
    $(this).hide();
    var img = $(this).find(".board_food");
    food_dict[img.attr("src")].show();
  });

  //右侧菜单内食物的点击事件
  $(".ingredient").click(function () {
    $(this).hide();
    src = $(this).attr("src");
    food_dict[src] = $(this);
    var add = '<a class="thumb">' +
                '<img class="board_food" src="' + src + '" alt="' + $(this).attr("alt") + '">' +
                '<div class="mask">' +
                '</div>'
              '</a>';
    $(".mk_board").append(add);

  });
  $("#color_filter li").click(function () {
    if($(this).hasClass("selected")) {
      $(this).removeClass("selected");
      $("#ingredient_select img").show();
    } else {
      $("#ingredient_select img").hide();
      $("#ingredient_select ." + $(this).attr("color-type")).show();
      $("#color_filter li").removeClass("selected");
      $(this).addClass("selected");
    }
  });

});
