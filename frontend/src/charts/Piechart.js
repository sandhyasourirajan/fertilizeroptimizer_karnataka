export function generate_pie_chart(piechart_view,chart_container,Chartdata) {

  if (!piechart_view) {
    // console.log(Chartdata)
    // console.log("div:",chart_container)
    piechart_view = d3plus.viz()
      .container(chart_container)
      .data(Chartdata)
      .type("pie")
      .id("name")
      .size("value")
      .background("#ffe0cc")
      .color("hex")
      .tooltip(["value"])
    }
    else {
    // Re-plot
    piechart_view
        .data(Chartdata)
        .id("name")
}
    return piechart_view

  }
