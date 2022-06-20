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


// assign red_detect = 	 	((8'd0 <= hue) & (hue <9'd40) | (9'd345 < hue) & (hue <= 9'd360))  & 
// 							(8'd174 < sat) & (sat < 8'd255) & (8'd110 < val) & (val <= 8'd255);
							
// assign pink_detect = ((hue > 9'd8) & (hue < 9'd36) & (sat > 8'd93) & (sat < 8'd160) & (val > 8'd170) & (val <= 8'd255));
							

// assign green_detect =  		((((9'd104 < hue) & (hue < 9'd166) & (8'd40 < sat) & (sat < 8'd127)) | ((9'd120 < hue) & (hue < 9'd166) & (8'd62 < sat) & (sat < 8'd197))) & (val > 8'd30)&(val < 8'd165));

// assign lightgreen_detect = ((hue > 9'd93) & (hue < 9'd122) & (sat > 8'd99) & (sat < 8'd190) & (val > 8'd170) & (val <= 8'd255));

// assign yellow_detect = ((9'd52 < hue) & (hue < 9'd64) & (8'd100 < sat) & (sat < 8'd190) & (val <= 8'd255) & (val > 8'd190));

// assign darkblue_detect = ((9'd170 < hue) & (hue < 9'd235) & (sat > 8'd25) & (sat < 8'd175) & (val < 8'd140) & (8'd30 < val));

assign red_detect = 	 	((8'd0 <= hue) & (hue <9'd40) | (9'd345 < hue) & (hue <= 9'd360))  & 
							(8'd174 < sat) & (sat < 8'd255) & (8'd110 < val) & (val <= 8'd255);
							
assign pink_detect = ((hue > 9'd8) & (hue < 9'd36) & (sat > 8'd93) & (sat < 8'd160) & (val > 8'd170) & (val <= 8'd255));
							

assign green_detect =  		((((9'd104 < hue) & (hue < 9'd160) & (8'd40 < sat) & (sat < 8'd127)) | ((9'd120 < hue) & (hue < 9'd166) & (8'd62 < sat) & (sat < 8'd197))) & (val > 8'd30)&(val < 8'd165));

assign lightgreen_detect = ((hue > 9'd93) & (hue < 9'd122) & (sat > 8'd99) & (sat < 8'd190) & (val > 8'd170) & (val <= 8'd255));

assign yellow_detect = ((9'd52 < hue) & (hue < 9'd64) & (8'd100 < sat) & (sat < 8'd190) & (val <= 8'd255) & (val > 8'd190));

assign darkblue_detect = ((9'd170 < hue) & (hue < 9'd235) & (sat > 8'd25) & (sat < 8'd175) & (val < 8'd140) & (8'd30 < val));






assign black_detect = (val < 8'd30);

assign white_detect = ((sat < 8'd114) & (val > 8'd204));



endmodule