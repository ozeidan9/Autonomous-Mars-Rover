module colour_detect(
	input [8:0] hue,
	input [7:0] sat,
	input [7:0] val,
	output red_detect,
	output green_detect,
	output yellow_detect,
	output darkblue_detect,
	output pink_detect, 
	output lightgreen_detect,
	output black_detect,
	output white_detect
	//add for more colour detections:
);

//red, green, yellow, dark blue, pink, light green

// assign red_detect = 		((9'd345 < hue) & (hue <= 8'd360) | (8'd0 <= hue) & (hue < 8'd15)) & 
// 							((8'd60 < sat) & (8'd60 < val));
							
							

// assign green_detect =  		((9'd60 < hue) & (hue < 9'd160 )) & 
// 							((8'd60 < sat)  & (8'd60 < val))  
// 							;

// assign pink_detect =  	((9'd60 < hue) & (hue < 9'd160 )) & 
// 							((8'd60 < sat)  & (8'd60 < val))  
// 							;

// assign red_detect = 		((9'd345 < hue) & (hue <= 8'd360) | (8'd0 <= hue) & (hue < 8'd15)) & 
// 							((8'd155 < sat) & (8'd100 < val));
							
							

// assign green_detect =  		((9'd60 < hue) & (hue < 9'd165 )) & 
// 							((8'd70 < sat)  & (8'd40 < val));

// assign pink_detect = 		(((9'd308 < hue) & (hue <= 8'd360)) | ((8'd0 <= hue) & (hue < 8'd22))) & 
// 							(((8'd56 < sat) & (sat < 8'd155)) & (8'd137 < val));

assign red_detect = 		((9'd345 < hue) & (hue <= 8'd360) | (8'd0 <= hue) & (hue < 8'd15)) & 
							((8'd155 < sat) & (8'd100 < val));
							
							

assign green_detect =  		((9'd101 < hue) & (hue < 9'd153)) & 
							((8'd109 < sat) & (sat < 8'd169)) & (val < 8'd159);

assign pink_detect = 		(((9'd308 < hue) & (hue <= 8'd360)) | ((8'd0 <= hue) & (hue < 8'd22))) & 
							(((8'd56 < sat) & (sat < 8'd155)) & (8'd137 < val));




assign black_detect = (val < 8'd70) & (sat < 8'd55);

assign white_detect = ((sat < 8'd70) & (val > 8'd200));



endmodule