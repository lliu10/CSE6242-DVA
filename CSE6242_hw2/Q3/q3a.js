
	    global_width = 1000,
	    global_height = 500;

	    // define the dimensions and margins for the graph
	    var margin = {top:100, right: 200, bottom: 50, left: 150}; 
	    var width = global_width - margin.left - margin.right, 
	        height = global_height - margin.top - margin.bottom; 


		//Appending first SVG element
		var svg1 = d3.select("body").append("svg1")
					.attr('width', global_width)
					.attr('height', global_height)
					.append("g")
					.attr("transform", "translate(80,20)");

		//Set colors using schemeCategory10
		var colors = d3.schemeCategory10;

		d3.dsv(',', 'boardgame_ratings.csv', function(d){
			return{
				date: d3.timeParse("%Y-%m-%d")(d.date), //Parsing string to time obj
				Catan_count: +d['Catan=count'],
				Dominion_count: +d['Dominion=count'],
				Codenames_count: +d['Codenames=count'],
				Teraforming_Mars: +d['Terraforming Mars=count'],
				Gloomhaven_count: +d['Gloomhaven=count'],
				Magic_count: +d['Magic: The Gathering=count'],
				Dixit_count: +d['Dixit=count'],
				Monopoly_count: +d['Monopoly=count']

			}

			}).then(function(data){
			
					var timeFormatter = d3.timeFormat('%b %y') //format time

					var keys = ['Catan_count', 
								'Dominion_count', 
								'Codenames_count', 
								'Teraforming_Mars', 
								'Gloomhaven_count', 
								'Magic_count',
								'Dixit_count', 
								'Monopoly_count'],

						
						legend = ['Catan', 
								  'Dominion', 
								  'Codenames', 
								  'Terraforming Mars', 
								  'Gloomhaven', 
								  'Magic: The Gathering', 
								  'Dixit', 
								  'Monopoly'];					


						all_values = [];

						for(i = 0; i < data.length; i++){
							for (j = 0; j < keys.length; j++){
								all_values.push(data[i][keys[j]])
								
							}
						} 




					//Scales 
					const xScale = d3.scaleTime().range([0, width]),
						  yScale = d3.scaleLinear().rangeRound([height, 0]);

					xScale.domain(d3.extent(data, function(d){	
						return d.date})) // [Tue Nov 01 2016 00:00:00 GMT-0700 (Pacific Daylight Time), Sat Aug 01 2020 00:00:00 GMT-0700 (Pacific Daylight Time)]

					yScale.domain([(0), d3.max(all_values)]) // [0, "95775"]


					//Declare x-axis and y-axis
					var xAxis = d3.axisBottom(xScale)
							  .tickFormat(d3.timeFormat('%b %y')),

						yaxis = d3.axisLeft(yScale)
								  .ticks(10);
							
					//Append axes
					svg1.append('g')
						.attr('class', 'x axis')
						.attr("transform", "translate(0," + height + ")")
						.call(xAxis);

					svg1.append('g')
						.attr('class', 'y axis')
						.call(yaxis);

					//Lines
					var lines = [];

					var Catan_line = d3.line()
									   .x(function(d){return xScale(d.date)}) 
									   .y(function (d) {return yScale(d.Catan_count)})
									   .curve(d3.curveMonotoneX);

					lines.push(Catan_line);

					var Dominion_line = d3.line()
										  .x(function(d){return xScale(d.date)})
										  .y(function(d){return yScale(d.Dominion_count)})
										  .curve(d3.curveMonotoneX);

					
					lines.push(Dominion_line);

					var Codenames_line = d3.line()
										  .x(function(d){return xScale(d.date)})
										  .y(function(d){return yScale(d.Codenames_count)})
										  .curve(d3.curveMonotoneX);

					lines.push(Codenames_line)

					var Mars_line = d3.line()
									  .x(function(d){return xScale(d.date)})
									  .y(function(d){return yScale(d.Teraforming_Mars)})
									  .curve(d3.curveMonotoneX);

					lines.push(Mars_line);

					var Gloomhaven_line = d3.line()
											.x(function(d){return xScale(d.date)})
											.y(function(d){return yScale(d.Gloomhaven_count)})
											.curve(d3.curveMonotoneX);

					lines.push(Gloomhaven_line);

					var Magic_line = d3.line()
										.x(function(d){return xScale(d.date)})
										.y(function(d){return yScale(d.Magic_count)})
										.curve(d3.curveMonotoneX);

					lines.push(Magic_line);

					var Dixit_line = d3.line()
										.x(function(d){return xScale(d.date)})
										.y(function(d){return yScale(d.Dixit_count)})
										.curve(d3.curveMonotoneX);

					lines.push(Dixit_line);

					var Monopoly_line = d3.line()
										.x(function(d){return xScale(d.date)})
										.y(function(d){return yScale(d.Monopoly_count)})
										.curve(d3.curveMonotoneX)



					lines.push(Monopoly_line);



					
					
					for (index = 0; index < lines.length; index++){

						svg1.append('path')
							.datum(data)
							.style("stroke", colors[index])
							.attr('class', 'line')
							.attr('id', function(d){return legend[index]})
							.attr('d', lines[index])
							// .append('text')
							// .attr('class', 'series_id')
							// .attr("x", function(d){return d.x})
							// .attr("y", function(d){return d.y})
							// .text(legend[index])
							

					}

					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 345)
					.attr('fill', colors[0])
					.text('Catan')

					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 270)
					.attr('fill', colors[1])
					.text('Dominion')


					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 225)
					.attr('fill', colors[2])
					.text('Codenames')


					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 203)
					.attr('fill', colors[3])
					.text('Terraforming Mars')


					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 130)
					.attr('fill', colors[4])
					.text('Gloomhaven')

					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 109)
					.attr('fill', colors[5])
					.text('Magic: The Gathering')

					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 170)
					.attr('fill', colors[6])
					.text('Dixit')

					svg1.append('g')
					.selectAll('line')
					.data(data)
					.enter()
					.append('text')
					.attr('x', width+3)
					.attr('y', height - 94)
					.attr('fill', colors[7])
					.text('Monopoly')


				//Chart Title 
				svg1.append('g')
				   .append('text')
				   .attr('id', 'title')
				   .attr("x", width/3)
				   .attr('y', height-355)
				   .attr("stroke", "black")
				   .text("Number of Ratings 2016 - 2020");


				})