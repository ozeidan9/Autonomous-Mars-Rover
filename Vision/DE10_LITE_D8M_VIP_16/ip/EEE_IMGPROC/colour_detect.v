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
//ARENA OLD
// assign red_detect = 	 	((8'd0 <= hue) & (hue < 9'd40) | (9'd340 < hue) & (hue <= 9'd360))  & 
// 							((8'd190 < sat) & (sat <= 8'd255) & (8'd60 < val) & (val <= 8'd190));
							
// assign pink_detect = (hue > 9'd0) & (hue < 9'd36) & (sat > 8'd93) & (sat < 8'd175) & (val > 8'd190) & (val <= 8'd255);
							

// assign green_detect =  		((((9'd104 < hue) & (hue < 9'd155) & (8'd40 < sat) & (sat < 8'd127)) | ((9'd120 < hue) & (hue < 9'd166) & (8'd62 < sat) & (sat < 8'd197))) & (val > 8'd30)&(val < 8'd130));

// assign lightgreen_detect = ((hue > 9'd93) & (hue < 9'd128) & (sat > 8'd99) & (sat < 8'd190) & (val > 8'd140) & (val <= 8'd255));

// assign yellow_detect = ((9'd52 < hue) & (hue < 9'd64) & (8'd100 < sat) & (sat < 8'd200) & (val <= 8'd255) & (val > 8'd190));

// assign darkblue_detect = ((9'd170 < hue) & (hue < 9'd235) & (sat > 8'd25) & (sat < 8'd175) & (val < 8'd140) & (8'd30 < val));

//////////////////////
//ARENA THRESHOLDS////

assign red_detect = ((8'd0 <= hue) & (hue < 9'd40) | (9'd340 < hue) & (hue <= 9'd360)) &
((8'd165 < sat) & (sat <= 8'd255) & (8'd45 < val) & (val <= 8'd175)); //saturation is almost independant of location (95/100)
							
assign pink_detect = (hue > 9'd0) && (hue < 9'd36) && (sat > 8'd105) && (sat <= 8'd150) && (val > 8'd185) && (val <= 8'd255);
							

assign green_detect =  		((((9'd104 < hue) & (hue < 9'd155) & (8'd40 < sat) & (sat < 8'd127)) | ((9'd120 < hue) & (hue < 9'd166) & (8'd62 < sat) & (sat < 8'd197))) & (val > 8'd30)&(val < 8'd130));

assign lightgreen_detect = ((hue > 9'd93) & (hue < 9'd128) & (sat > 8'd99) & (sat < 8'd190) & (val > 8'd120) & (val <= 8'd255));

assign yellow_detect = ((9'd52 < hue) & (hue < 9'd64) & (8'd100 < sat) & (sat < 8'd200) & (val <= 8'd255) & (val > 8'd190));

assign darkblue_detect = ((9'd170 < hue) & (hue < 9'd235) & (sat > 8'd25) & (sat < 8'd175) & (val < 8'd140) & (8'd40 < val));





///////////////
//TESTING THRESHOLDSS///

// assign red_detect = 	 	((8'd0 <= hue) & (hue <9'd40) | (9'd345 < hue) & (hue <= 9'd360))  & 
// 							(8'd170 < sat) & (sat < 8'd255) & (8'd100 < val) & (val <= 8'd255);
							
// assign pink_detect = (hue > 9'd0) & (hue < 9'd36) & (sat > 8'd93) & (sat < 8'd196) & (val > 8'd235) & (val <= 8'd255);
							

// assign green_detect =  		((((9'd104 < hue) & (hue < 9'd155) & (8'd40 < sat) & (sat < 8'd127)) | ((9'd120 < hue) & (hue < 9'd166) & (8'd62 < sat) & (sat < 8'd197))) & (val > 8'd30)&(val < 8'd130));

// assign lightgreen_detect = ((hue > 9'd93) & (hue < 9'd128) & (sat > 8'd99) & (sat < 8'd190) & (val > 8'd140) & (val <= 8'd255));

// assign yellow_detect = ((9'd52 < hue) & (hue < 9'd64) & (8'd100 < sat) & (sat < 8'd200) & (val <= 8'd255) & (val > 8'd190));

// assign darkblue_detect = ((9'd170 < hue) & (hue < 9'd235) & (sat > 8'd25) & (sat < 8'd175) & (val < 8'd140) & (8'd40 < val));





assign black_detect = (val < 8'd30);

assign white_detect = ((sat < 8'd114) & (val > 8'd204));



endmodule