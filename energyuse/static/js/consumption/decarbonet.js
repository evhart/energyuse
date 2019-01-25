require(["common"], function(_) {


	require(["dc","lib/crossfilter", "lib/reductio"], function(dc,crossfilter,reducito) {
	    //This function is called when scripts/helper/util.js is loaded.
	    //If util.js calls define(), then this function is not fired until
	    //util's dependencies have loaded, and the util argument will hold
	    //the module value for "helper/util".

		$(function() {




			//$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			var colors = ["#EFDECD", "#CD9575", "#FDD9B5", "#78DBE2", "#87A96B", "#FFA474", "#FAE7B5", "#9F8170", "#FD7C6E", "#000000", "#ACE5EE", "#1F75FE", "#A2A2D0", "#6699CC", "#0D98BA", "#7366BD", "#DE5D83", "#CB4154", "#B4674D", "#FF7F49", "#EA7E5D", "#B0B7C6", "#FFFF99", "#1CD3A2", "#FFAACC", "#DD4492", "#1DACD6", "#BC5D58", "#DD9475", "#9ACEEB", "#FFBCD9", "#FDDB6D", "#2B6CC4", "#EFCDB8", "#6E5160", "#CEFF1D", "#71BC78", "#6DAE81", "#C364C5", "#CC6666", "#E7C697", "#FCD975", "#A8E4A0", "#95918C", "#1CAC78", "#1164B4", "#F0E891", "#FF1DCE", "#B2EC5D", "#5D76CB", "#CA3767", "#3BB08F", "#FEFE22", "#FCB4D5", "#FFF44F", "#FFBD88", "#F664AF", "#AAF0D1", "#CD4A4C", "#EDD19C", "#979AAA", "#FF8243", "#C8385A", "#EF98AA", "#FDBCB4", "#1A4876", "#30BA8F", "#C54B8C", "#1974D2", "#FFA343", "#BAB86C", "#FF7538", "#FF2B2B", "#F8D568", "#E6A8D7", "#414A4C", "#FF6E4A", "#1CA9C9", "#FFCFAB", "#C5D0E6", "#FDDDE6", "#158078", "#FC74FD", "#F78FA7", "#8E4585", "#7442C8", "#9D81BA", "#FE4EDA", "#FF496C", "#D68A59", "#714B23", "#FF48D0", "#E3256B", "#EE204D", "#FF5349", "#C0448F", "#1FCECB", "#7851A9", "#FF9BAA", "#FC2847"];

				//console.log(dataURL);
				d3.csv(dataURL, function (data) {
				window.data = data;

				//TODO check if no data
					$("#consumption-loading").fadeOut();

					$("#consumption-visualisation").fadeIn();

				data = data.map(function (d) {
					//console.log(d);
					d.t = d3.time.format("%Y-%m-%d %H:%M:%S+00:00").parse(d.t);
					d.day = d3.time.day(d.t); // pre-calculate month for better performance
					d.consumption = +d.consumption; // coerce to number
					return d;
				});


				//Create the crossfiter object:
				window.ndx = crossfilter(data);
				window.all = ndx.groupAll();

				var yearlyDimension = ndx.dimension(function (d) {
					return d3.time.year(d.t).getFullYear();
				});


				//Groups
				byDay = ndx.dimension(function (d) {
					return d.day;
				});// d3.time.format("%Y-%m-%dT%H:%M:%S.000+0000").parse(d.date); })
				byDayGroup = byDay.group().reduceSum(function (d) {
					return d.consumption;
				});
				byDayGroup.all();

				byDay2 = ndx.dimension(function (d) {
					return d.day;
				});// d3.time.format("%Y-%m-%dT%H:%M:%S.000+0000").parse(d.date); })
				byDayGroup2 = byDay2.group().reduceSum(function (d) {
					return d.consumption;
				});
				byDayGroup2.all();


				var dayOfWeek = ndx.dimension(function (d) {
					var day = d.t.getDay();
					var name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
					return day + '.' + name[day];
				});
				//var dayOfWeekGroup = dayOfWeek.group().reduceSum(function(d){ return (d.consumption; });
				dayOfWeekGroup = dayOfWeek.group().reduce(
					function (p, v) {
						++p.count;
						p.total += v.consumption;
						return p;
					},
					function (p, v) {
						--p.count;
						p.total -= v.consumption;
						return p;
					},
					function () {
						return {total: 0, count: 0};
					});


				conceptDimAll = ndx.dimension(function (d) {
					return d.concept;
				});
				//conceptDimAll.filterFunction(function(d){ return d === 'all';});
				conceptDimGroupAll = conceptDimAll.group().reduceSum(function (d) {
					//console.log(d);
					return d.consumption;
				});

				day = ndx.dimension(function (d) {
					return +d.day;
				});
				conceptDim = ndx.dimension(function (d) {
					return d.concept;
				});
				conceptDim.filterFunction(function (d) {
					return d !== 'all';
				});


				//conceptDim.filter(function(v){console.log(v); v === "all";});


				cons = [];
				concepts = [];
				conceptDim.group().all().forEach(function (concept) {

					cons.push(concept.key);
					//concepts.push({'group': day.group().reduceSum(function(d){return d.concept==concept.key?d.consumption:0;}), 'concept': concept.key}); //sum
					concepts.push(day.group().reduceSum(function (d) {
						return d.concept == concept.key ? d.consumption : 0;
					})); //sum //TODO


					//concepts.push(day.group().reduceSum(function(d){return d.concept==concept.key?1:0;})); //occurances
				});


				compose = dc.compositeChart("#serie")
					//.width(990) // (optional) define chart width, :default = 200
					.height(295)
					.dimension(day)
					.elasticY(true)
					.renderHorizontalGridLines(true)
					.x(d3.time.scale().domain([d3.time.day.offset(new Date(data[0].t), -0.5), d3.time.day.offset(new Date(data[data.length - 1].t), 0)]))
					.xUnits(d3.time.days)
					.group(concepts[1]);





				moveChart = dc.barChart(compose)
					.round(d3.time.day.round)
					.xUnits(d3.time.days)
					.ordinalColors(colors)
					.gap(0)
					.centerBar(true)
					.group(concepts.shift(), cons.shift()); //put the first one


				for (var i = 0; i < concepts.length; i++) {
					moveChart.stack(concepts[i], cons[i]);
				}


				var volumeChart = dc.barChart("#serie2")
					.width(990) // (optional) define chart width, :default = 200
					.height(75);

				volumeChart.margins({top: 0, right: 50, bottom: 20, left: 40})
					.dimension(byDay2)
					.group(byDayGroup2)
					.centerBar(true)
					.ordinalColors(['#fdb462'])
					.gap(1)
					//.xAxisLabel("Date")
					//.elasticX(true)
					.x(d3.time.scale().domain([d3.time.day.offset(new Date(data[0].t), -0.5), d3.time.day.offset(new Date(data[data.length - 1].t), 0)]))
					.round(d3.time.day.round)
					.xUnits(d3.time.days)
					.renderlet(function (chart) {
						chart.select("g.y").style("display", "none");
						moveChart.filter(chart.filter());
					})
					.on("filtered", function (chart) {
						dc.events.trigger(function () {
							compose.focus(chart.filter());
						});
					});
				volumeChart.render();


				//////////////////////////////////////////////////////////////////
				//Appliances distribution
				window.dc = dc;
				//conceptDim2 = ndx.dimension(function(d){return Math.round(Math.random(5)*5)+1 /*d.concept*/;});
				conceptDim2 = ndx.dimension(function (d) {
					return d.concept;
				});
				conceptGroup = conceptDim2.group().reduceSum(function (d) {
					return d.consumption;
				});//Math.round(d.consumption *1000);});


				pie = dc.pieChart("#pie");
				pie.width(200).height(200)
					.innerRadius(50)
					.dimension(conceptDim2)
					.group(conceptGroup)
					.ordinalColors(colors);


				//////////////////////
				//dataAll
				// line = dc.lineChart(compose)
				// 	.dimension(day)
				// 	.useRightYAxis(true)
				// 	.dashStyle([5,5])
				// 	.ordinalColors(['#fdb462'])
				// 	.elasticY(false)
				// 	.elasticX(false)
				// 	.group(conceptDimGroupAll,"Total Consumption"); //put the first one
				// 	//.group(conceptDimGroupAll,"Total Consumption"); //put the first one


				// bars = dc.barChart(compose)
				// 	 .centerBar(true)
				// 	 .gap(100)
				// 	 .group(concepts[1]);


				dayOfWeekChart = dc.rowChart('#day-of-week-chart')
					.width(180)
					.height(180)
					.margins({top: 20, left: 10, right: 10, bottom: 20})
					.group(dayOfWeekGroup)
					.dimension(dayOfWeek)
					.ordinalColors(['#30BA8F', '#30ba5b', '#5cba30', '#8eba30', '#b3ba30'])
					.label(function (d) {
						return d.key.split('.')[1];
					})
					.valueAccessor(function (p) {
						if (p.value.total === 0 || p.value.count === 0) {
							return 0;
						} else {
							return p.value.total / p.value.count;
						}
					})
					.elasticX(true);

					dayOfWeekChart.xAxis().ticks(4);


				//var heightOfContainer = 500,
    				//legendHeight = 150,
    				//legendY = heightOfContainer - legendHeight;
                //
				//var chart = dc.lineChart('#parent');
				//chart.margins().bottom = legendY + 10; // 10 for padding.
				//chart.legend(dc.legend().y(legendY));
				//

				compose.compose([moveChart/*,line*/])
					.brushOn(false)
					.elasticY(false)
					.elasticX(false)
					.yAxisLabel("Daily Appliances Consumption  (kWh)")
					// .rightYAxisLabel("Daily Total Consumption  (kWh)")
					.legend(dc.legend().x(50).y(10)
						//.xAxis().tickFormat(function(d){ return d; })
						// .yAxisLabel("Appliances Consumption")
						//.rightYAxisLabel("Total Consumption")
						//.xAxis()
						//.ticks(d3.time.days)
						//.tickFormat(function(d) {
						//			 return (d.getMonth() + 1) + "/" + d.getFullYear();
						//	})
						.itemHeight(13).gap(5));

					 var newWidth1 = document.getElementById('serie').parentNode.offsetWidth;
					  var newWidth2 = document.getElementById('pie').parentNode.offsetWidth;

					  compose.width(newWidth1).transitionDuration(0);
					  volumeChart.width(newWidth1).transitionDuration(0);
					  pie.width(newWidth2).transitionDuration(0);
					  dayOfWeekChart.width(newWidth2).transitionDuration(0);

					 compose.transitionDuration(750);
					  volumeChart.transitionDuration(750);
					  pie.transitionDuration(750);
					  dayOfWeekChart.transitionDuration(750);

				dc.renderAll();



				window.onresize = function(event) {
					  //alert("dasdas");
					  var newWidth1 = document.getElementById('serie').parentNode.offsetWidth;
					  var newWidth2 = document.getElementById('pie').parentNode.offsetWidth;

					  compose.width(newWidth1).transitionDuration(0);
					  volumeChart.width(newWidth1).transitionDuration(0);
					  pie.width(newWidth2).transitionDuration(0);
					  dayOfWeekChart.width(newWidth2).transitionDuration(0);


					  dc.renderAll();
					  //dc.redraw()
					  compose.transitionDuration(750);
					  volumeChart.transitionDuration(750);
					  pie.transitionDuration(750);
					  dayOfWeekChart.transitionDuration(750);

					};
			});

			//});
		});
	});
});
