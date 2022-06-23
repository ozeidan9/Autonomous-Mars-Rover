module EEE_IMGPROC(
    // global clock & reset
    clk,
    reset_n,
    // mm slave
    s_chipselect,
    s_read,
    s_write,
    s_readdata,
    s_writedata,
    s_address,
    // stream sink
    sink_data,
    sink_valid,
    sink_ready,
    sink_sop,
    sink_eop,
    // streaming source
    source_data,
    source_valid,
    source_ready,
    source_sop,
    source_eop,
    // conduit
    mode,
    outbuffer,
    byte_data_received
    

);


// global clock & reset
input   clk;
input   reset_n;
// mm slave
input                           s_chipselect;
input                           s_read;
input                           s_write;
output  reg [31:0]  s_readdata;
input   [31:0]              s_writedata;
input   [2:0]                   s_address;
// streaming sink
input   [23:0]              sink_data;
input                               sink_valid;
output                          sink_ready;
input                               sink_sop;
input                               sink_eop;
// streaming source
output  [23:0]                 source_data;
output                              source_valid;
input                                   source_ready;
output                              source_sop;
output                              source_eop;
// conduit export ANTHONY ADDED EVERYTHING HERE EXCEPT FOR MODE
input                         mode;
output reg[15:0]                   outbuffer;
input[15:0]                  byte_data_received;
////////////////////////////////////////////////////////////////////////
//
parameter IMAGE_W = 11'd640;
parameter IMAGE_H = 11'd480;
parameter MESSAGE_BUF_MAX = 256;
parameter MSG_INTERVAL = 6;
parameter BB_COL_DEFAULT = 24'h00ff00;
wire [7:0]   red, green, blue, grey;
wire [7:0]   red_out, green_out, blue_out;
wire         sop, eop, in_valid, out_ready;

reg red_found, green_found, yellow_found, darkblue_found, pink_found, lightgreen_found; // need to do for others...
reg[10:0] max_width;
reg distance_measure_active;
reg r_ball_registered, g_ball_registered, y_ball_registered, p_ball_registered, db_ball_registered, lg_ball_registered;

reg r_ball_watching, g_ball_watching, y_ball_watching, p_ball_watching, db_ball_watching, lg_ball_watching;

reg r_in_frame, r_prev_frame1, r_prev_frame2, r_prev_frame3;
reg g_in_frame, g_prev_frame1, g_prev_frame2, g_prev_frame3;
reg y_in_frame, y_prev_frame1, y_prev_frame2, y_prev_frame3;
reg p_in_frame, p_prev_frame1, p_prev_frame2,p_prev_frame3 ;
reg db_in_frame, db_prev_frame1, db_prev_frame2, db_prev_frame3;
reg lg_in_frame, lg_prev_frame1, lg_prev_frame2, lg_prev_frame3;
reg[10:0] r_width, y_width, g_width, p_width, db_width, lg_width, r_height;
reg[10:0] r_width1, y_width1, g_width1, p_width1, db_width1, lg_width1;
reg[10:0] r_width2, y_width2, g_width2, p_width2, db_width2, lg_width2;
reg[10:0] r_width3, y_width3, g_width3, p_width3, db_width3, lg_width3;

reg [10:0] r_width_check, r_height_check;
reg [10:0] g_width_check, g_height_check;
reg [10:0] lg_width_check, lg_height_check;
reg[2:0] no_red_ball_counter;

initial begin
    no_red_ball_counter = 0;
    red_found = 0;
    green_found = 0;
    yellow_found = 0;
    pink_found = 0;
    darkblue_found = 0;
    lightgreen_found = 0;

    outbuffer = 0;
    r_ball_registered = 0;
    y_ball_registered = 0;
    g_ball_registered = 0;
    p_ball_registered = 0;
    db_ball_registered = 0;
    lg_ball_registered = 0;

    r_ball_watching = 0;
    g_ball_watching = 0;
    y_ball_watching = 0;
    p_ball_watching = 0;
    db_ball_watching = 0;
    lg_ball_watching = 0;

    r_in_frame = 0;
    r_prev_frame1 = 0;
    r_prev_frame2 = 0;
    r_prev_frame3 = 0;
    g_in_frame = 0;
    g_prev_frame1 = 0;
    g_prev_frame2 = 0;
    g_prev_frame3 = 0;
    y_in_frame = 0;
    y_prev_frame1 = 0;
    y_prev_frame2 = 0;
    y_prev_frame3 = 0;
    p_in_frame = 0;
    p_prev_frame1 = 0;
    p_prev_frame2 = 0;
    p_prev_frame3 = 0;
    db_in_frame = 0;
    db_prev_frame1 = 0;
    db_prev_frame2 = 0;
    db_prev_frame3 = 0;
    lg_in_frame = 0;
    lg_prev_frame1 = 0;
    lg_prev_frame2 = 0;
    lg_prev_frame3 = 0;

    distance_measure_active = 0;

    r_width = 0;
    y_width = 0;
    g_width = 0;
    p_width = 0;
    db_width = 0;
    lg_width = 0;
        
    r_width1 = 0;
    y_width1 = 0;
    g_width1 = 0;
    p_width1 = 0;
    db_width1 = 0;
    lg_width1 = 0;
    
    r_width2 = 0;
    y_width2 = 0;
    g_width2 = 0;
    p_width2 = 0;
    db_width2 = 0;
    lg_width2 = 0;
    
    r_width3 = 0;
    y_width3 = 0;
    g_width3 = 0;
    p_width3 = 0;
    db_width3 = 0;
    lg_width3 = 0;
    
    r_height = 0;

    r_width_check = 0;
    r_height_check = 0;
    g_width_check = 0;
    g_height_check = 0;
    lg_width_check = 0;
    lg_height_check = 0;
end 


always @(posedge clk) begin
    if(byte_data_received == 1)begin
        r_ball_registered <= 1;
    end
    if (y > 476)begin
        r_prev_frame3 <=  r_prev_frame2 & (r_width3 < r_width2 + 10) & (r_width3 > r_width2 - 10) & (r_height > 25);
        r_prev_frame2 <=  r_prev_frame1 & (r_width2 < r_width1 + 10) & (r_width2 > r_width1 - 10) & (r_height > 25);
        r_prev_frame1 <= red_found & (r_width1 < r_width + 10) & (r_width1 > r_width - 10) & (r_width > 40) & (r_height > 25);
    
        g_prev_frame3 <=  g_prev_frame2  & ((g_width3 < g_width2 + 10) & (g_width3 > g_width2 - 10)) ;
        g_prev_frame2 <=  g_prev_frame1 & ((g_width2 < g_width1 + 10) & (g_width2 > g_width1 - 10));
        g_prev_frame1 <=  green_found & ((g_width1 < g_width + 10) & (g_width1 > g_width - 10));
    
        y_prev_frame3 <=  y_prev_frame2; //& ((y_width3 < y_width2 + 10) & (y_width3 > y_width2 - 10));
        y_prev_frame2 <=  y_prev_frame1; //& ((y_width2 < y_width1 + 10) & (y_width2 > y_width1 - 10));
        y_prev_frame1 <=  (y_width > 0); //& ((y_width1 < y_width + 10) & (y_width1 > y_width - 10));

        p_prev_frame3 <=  p_prev_frame2; //& ((p_width3 < p_width2 + 10) & (p_width3 > p_width2 - 10));
        p_prev_frame2 <=  p_prev_frame1; //& ((p_width2 < p_width1 + 10) & (p_width2 > p_width1 - 10));
        p_prev_frame1 <=  (p_width > 0); //& ((p_width1 < p_width + 10) & (p_width1 > p_width - 10));

        db_prev_frame3 <=  db_prev_frame2; //& ((db_width3 < db_width2 + 10) & (db_width3 > db_width2 - 10));
        db_prev_frame2 <=  db_prev_frame1; //& ((db_width2 < db_width1 + 10) & (db_width2 > db_width1 - 10));
        db_prev_frame1 <=  (db_width > 0); //& ((db_width1 < db_width + 10) & (db_width1 > db_width - 10));

        lg_prev_frame3 <=  lg_prev_frame2; //& ((lg_width3 < lg_width2 + 10) & (lg_width3 > lg_width2 - 10));
        lg_prev_frame2 <=  lg_prev_frame1; //& ((lg_width2 < lg_width1 + 10) & (lg_width2 > lg_width1 - 10));
        lg_prev_frame1 <=  (lg_width > 0); //& ((lg_width1 < lg_width + 10) & (r_width1 > lg_width - 10));
        r_height <= r_y_max - r_y_min;
        if (r_in_frame)begin
            if (r_x_max - r_x_min < r_width + 10 & r_x_max-r_x_min > r_width - 10)begin
                r_width <= r_x_max - r_x_min;
            end
        end
        else begin
            r_width <= r_x_max - r_x_min;
        end
        
        r_width <= r_x_max - r_x_min;
        r_width3 <= r_width2;
        r_width2 <= r_width1;
        r_width1 <= r_width; 
        g_width <= g_x_max - g_x_min;
        g_width3 <= g_width2;
        g_width2 <= g_width1;
        g_width1 <= g_width; 
        y_width <= y_x_max - y_x_min;
        y_width3 <= y_width2;
        y_width2 <= y_width1;
        y_width1 <= y_width; 
        p_width <= p_x_max - p_x_min;
        p_width3 <= p_width2;
        p_width2 <= p_width1;
        p_width1 <= p_width; 
        db_width <= db_x_max - db_x_min;
        db_width3 <= db_width2;
        db_width2 <= db_width1;
        db_width1 <= db_width; 
        lg_width <= lg_x_max - lg_x_min;
        lg_width3 <= lg_width2;
        lg_width2 <= lg_width1;
        lg_width1 <= lg_width;

        r_in_frame <= r_prev_frame1 & r_prev_frame2 & r_prev_frame3;
        g_in_frame <= g_prev_frame1 & g_prev_frame2 & g_prev_frame3;
        y_in_frame <= y_prev_frame1 & y_prev_frame2 & y_prev_frame3;
        p_in_frame <= p_prev_frame1 & p_prev_frame2 & p_prev_frame3;
        db_in_frame <= db_prev_frame1 & db_prev_frame2 & db_prev_frame3;
        lg_in_frame <= lg_prev_frame1 & lg_prev_frame2 & lg_prev_frame3;    

    end
    r_width_check <= r_x_max - r_x_min;
    r_height_check <= r_y_max - r_y_min;
    g_width_check <= g_x_max - g_x_min;
    g_height_check <= g_y_max - g_y_min;
    lg_width_check <= lg_x_max - lg_x_min;
    lg_height_check <= lg_y_max - lg_y_min;
end




always @(*)begin
    if(distance_measure_active == 0)begin
        no_red_ball_counter = 0;
        outbuffer = 0;
        max_width = 11'd5;
        if (r_in_frame & (r_width > max_width) & (r_ball_registered == 0))begin
            r_ball_watching = 1;
            max_width = r_width;
            distance_measure_active = 1;
        end
        if (g_in_frame & (g_width > max_width)  & ~g_ball_registered)begin
            g_ball_watching = 1;
            max_width = g_width;
            distance_measure_active = 1;
            r_ball_watching = 0;
        end
        if (y_in_frame & y_width > max_width  & ~y_ball_registered)begin
            y_ball_watching = 1;
            max_width = y_width;
            distance_measure_active = 1;
            r_ball_watching = 0;
            g_ball_watching = 0;
        end
        if (p_in_frame & p_width > max_width  & ~p_ball_registered)begin
            p_ball_watching = 1;
            max_width = p_width;
            distance_measure_active = 1;
            r_ball_watching = 0;
            g_ball_watching = 0;
            y_ball_watching = 0;
        end
        if (db_in_frame & db_width > max_width  & ~db_ball_registered)begin
            db_ball_watching = 1;
            max_width = db_width;
            distance_measure_active = 1;
            r_ball_watching = 0;
            g_ball_watching = 0;
            y_ball_watching = 0;
            p_ball_watching = 0;
        end

        if (lg_in_frame & lg_width > max_width  & ~lg_ball_registered)begin
            lg_ball_watching = 1;
            max_width = lg_width;
            distance_measure_active = 1;
            r_ball_watching = 0;
            g_ball_watching = 0;
            y_ball_watching = 0;
            p_ball_watching = 0;
            db_ball_watching = 0;
        end
    end
    
    else if(distance_measure_active == 1)begin
        if(r_ball_watching == 1)begin //identifier for red: 1
            if(r_ball_registered == 1)begin //if we have already found a red ball
                outbuffer = 0;
                r_ball_watching = 0;
                distance_measure_active = 0;
            end
            else if (no_red_ball_counter > 3)begin //if there is not actually a ball in sight
                outbuffer = 0;
                r_ball_watching = 0;
                distance_measure_active = 0;
            end
            else if (r_left == 0 & r_right == 0 & r_top == 0 & r_bottom == 0)begin
                no_red_ball_counter = no_red_ball_counter + 1;
            end
            else begin //otherwise there is a ball and we send r_ball_distance
                no_red_ball_counter = 0;
                outbuffer = (y == 476) ? r_ball_distance : outbuffer;
            end
            
        end
        
        else if(g_ball_watching == 1)begin //identifier for green: 2
            if(byte_data_received == 2)begin
                outbuffer = 0;
                g_ball_registered = 1;
                g_ball_watching = 0;
                distance_measure_active = 0;
            end
            else begin
                outbuffer = ((y > IMAGE_H-11'h8))  ? g_ball_distance : outbuffer;
            end
        end

        else if(y_ball_watching == 1)begin //identifier for yellow: 3
            if(byte_data_received >=3)begin
                outbuffer = 0;
                y_ball_registered = 1;
                y_ball_watching = 0;
                distance_measure_active = 0;
            end
            else begin
                outbuffer = ((y > IMAGE_H-11'h8))  ? y_ball_distance : outbuffer;
            end
        end

        else if(p_ball_watching == 1)begin //identifier for pink: 4
            if(byte_data_received == 4)begin
                outbuffer = 0;
                p_ball_registered = 1;
                p_ball_watching = 0;
                distance_measure_active = 0;
            end
            else begin
                outbuffer = ((y > IMAGE_H-11'h8))  ? p_ball_distance : outbuffer;
            end
        end

        else if(db_ball_watching == 1)begin //identifier for dark blue: 5
            if(byte_data_received == 5)begin
                outbuffer = 0;
                db_ball_registered = 1;
                db_ball_watching = 0;
                distance_measure_active = 0;
            end
            else begin
                outbuffer = ((y > IMAGE_H-11'h8))  ? db_ball_distance : outbuffer;
            end
        end

        else if(lg_ball_watching == 1)begin //identifier for light green: 6
            if(byte_data_received == 1)begin
                outbuffer = 0;
                lg_ball_registered = 1;
                lg_ball_watching = 0;
                distance_measure_active = 0;
            end
            else begin
                outbuffer = ((y > IMAGE_H-11'h8))  ? lg_ball_distance : outbuffer;
            end
        end
    end

end




//end
////////////////////////////////////////////////////////////////////////
// Detect red areas
wire red_detect;
wire green_detect;
wire yellow_detect;
wire darkblue_detect;
wire pink_detect;
wire lightgreen_detect;
wire black_detect;
wire white_detect;
wire building_detect;

// assign white_detect = (green>210) & (red>210) &  (blue>210); 
// assign black_detect = (green<50) & (red<50) &  (blue<50);
// Find boundary of cursor box
reg prev_r1, prev_r2, prev_r3, prev_r4;
reg prev_g1, prev_g2, prev_g3, prev_g4;
reg prev_y1, prev_y2, prev_y3, prev_y4;
reg prev_db1, prev_db2, prev_db3, prev_db4;
reg prev_p1, prev_p2, prev_p3, prev_p4;
reg prev_lg1, prev_lg2, prev_lg3, prev_lg4;
reg prev_b1, prev_b2, prev_b3, prev_b4;
reg prev_w1, prev_w2, prev_w3, prev_w4;

wire [7:0] sat, val, min;
wire [8:0] hue;
rgb_to_hsv conv(
    .green(green),
    .red(red),
    .blue(blue),
    .hue(hue),
    .min(min),
    .sat(sat),
    .value(val)
);
initial begin
    prev_r1 <= 0;
    prev_r2 <= 0;
    prev_r3 <= 0;
    prev_r4 <= 0;
    prev_g1 <= 0;
    prev_g2 <= 0;
    prev_g3 <= 0;
    prev_g4 <= 0;
    prev_y1 <= 0;
    prev_y2 <= 0;
    prev_y3 <= 0;
    prev_y4 <= 0;
    prev_db1 <= 0;
    prev_db2 <= 0;
    prev_db3 <= 0;
    prev_db4 <= 0;
    prev_p1 <= 0;
    prev_p2 <= 0;
    prev_p3 <= 0;
    prev_p4 <= 0;
    prev_lg1 <= 0;
    prev_lg2 <= 0;
    prev_lg3 <= 0;
    prev_lg4 <= 0;
    prev_b1 <= 0;
    prev_b2 <= 0;
    prev_b3 <= 0;
    prev_b4 <= 0;
    prev_w1 <= 0;
    prev_w2 <= 0;
    prev_w3 <= 0;
    prev_w4 <= 0;
end
always @(negedge clk)begin
    prev_r4 <= prev_r3;
    prev_r3 <= prev_r2;
    prev_r2 <= prev_r1;
    prev_r1 <= red_detect;
    prev_g4 <= prev_g3;
    prev_g3 <= prev_g2;
    prev_g2 <= prev_g1;
    prev_g1 <= green_detect;
    prev_y4 <= prev_y3;
    prev_y3 <= prev_y2;
    prev_y2 <= prev_y1;
    prev_y1 <= yellow_detect;
    prev_db4 <= prev_db3;
    prev_db3 <= prev_db2;
    prev_db2 <= prev_db1;
    prev_db1 <= darkblue_detect;
    prev_p4 <= prev_p3;
    prev_p3 <= prev_p2;
    prev_p2 <= prev_p1;
    prev_p1 <= pink_detect;
    prev_lg4 <= prev_lg3;
    prev_lg3 <= prev_lg2;
    prev_lg2 <= prev_lg1;
    prev_lg1 <= lightgreen_detect;
    prev_b4 <= prev_b3;
    prev_b3 <= prev_b2;
    prev_b2 <= prev_b1;
    prev_b1 <= black_detect;
    prev_w4 <= prev_w3;
    prev_w3 <= prev_w2;
    prev_w2 <= prev_w1;
    prev_w1 <= white_detect;
end
// Highlight detected areas
wire [23:0] detected_area;
assign grey = green[7:1] + red[7:2] + blue[7:2]; //Grey = green/2 + red/4 + blue/4


assign detected_area  =  //(black_detect & (x>7) & (x<640-7) & (y>7) & (y < 480-7) & prev_b1 & prev_b2 & prev_b3) ? {8'hd2, 8'h85, 8'h0} : 
                        // (white_detect & prev_w1 & prev_w2 & prev_w3) ? {8'h0, 8'h00, 8'hff} : 
                         (red_detect & prev_r1 & prev_r2 & prev_r3 & prev_r4) ? {8'hff, 8'h0, 8'h0} : 
                          (green_detect & prev_g1 & prev_g2 & prev_g3 & prev_g4) ? {8'h0, 8'hB1, 8'h0} :
                        //   (yellow_detect & prev_y1 & prev_y2 & prev_y3) ? {8'h00, 8'h63, 8'hA1} :
                        //  (darkblue_detect & prev_db1 & prev_db2 & prev_db3) ? {8'h00, 8'h63, 8'hA1} :
                        //   (pink_detect & prev_p1 & prev_p2 & prev_p3) ? {8'hFF, 8'h00, 8'hEF} :
                           (lightgreen_detect & prev_lg1 & prev_lg2 & prev_lg3 & prev_lg4) ? {8'h9A, 8'hE6, 8'h00} :
                         {grey, grey, grey};
                         
// Show bounding box
wire [23:0] new_image;
//defining the different types of BOUNDING BOXES
wire red_bb_active, green_bb_active, yellow_bb_active, darkblue_bb_active, pink_bb_active, lightgreen_bb_active ,black_bb_active, white_bb_active, build_bb_active;

// asssigning the different types of BOUNDING BOXES
// assign red_bb_active = (x == r_left) | (x == r_right) | (y == r_top) | (y == r_bottom);
assign red_bb_active = (((x == r_left & r_left != IMAGE_W-11'h1) | (x == r_right & r_right != 0)) & (r_bottom >= y & y >= r_top)) | (((y == r_top) | (y == r_bottom)) & (r_left <= x & x <= r_right));
assign green_bb_active = (((x == g_left & g_left != IMAGE_W-11'h1) | (x == g_right & g_right != 0)) & (g_bottom >= y & y >= g_top)) | (((y == g_top) | (y == g_bottom)) & (g_left <= x & x <= g_right));
assign yellow_bb_active = (((x == y_left & y_left != IMAGE_W-11'h1) | (x == y_right & y_right != 0)) & (y_bottom >= y & y >= y_top)) | (((y == y_top) | (y == y_bottom)) & (y_left <= x & x <= y_right));
assign darkblue_bb_active = (((x == db_left & db_left != IMAGE_W-11'h1) | (x == db_right & db_right != 0)) & (db_bottom >= y & y >= db_top)) | (((y == db_top) | (y == db_bottom)) & (db_left <= x & x <= db_right));
assign pink_bb_active = (((x == p_left & p_left != IMAGE_W-11'h1) | (x == p_right & p_right != 0)) & (p_bottom >= y & y >= p_top)) | (((y == p_top) | (y == p_bottom)) & (p_left <= x & x <= p_right));
assign lightgreen_bb_active = (((x == lg_left & lg_left != IMAGE_W-11'h1) | (x == lg_right & lg_right != 0)) & (lg_bottom >= y & y >= lg_top)) | (((y == lg_top) | (y == lg_bottom)) & (lg_left <= x & x <= lg_right));
//BUILDING BOUNDING BOXES   
assign black_bb_active = (((x == b_left & b_left != IMAGE_W-11'h1) | (x == b_right & b_right != 0)) & (b_bottom >= y & y >= b_top)) | (((y == b_top) | (y == b_bottom)) & (b_left <= x & x <= b_right));
assign white_bb_active = (((x == w_left & w_left != IMAGE_W-11'h1) | (x == w_right & w_right != 0)) & (w_bottom >= y & y >= w_top)) | (((y == w_top) | (y == w_bottom)) & (w_left <= x & x <= w_right));
assign build_bb_active = (x == build_left) | (x == build_right) | (y == build_top) | (y == build_bottom);

//--> ADD FOR THE OTHER BOUNDING BOXES
assign new_image =	red_bb_active ? {8'hdf,8'h16,8'h0} : 
                    green_bb_active ? {8'h0D, 8'h94, 8'h22} :
					//yellow_bb_active ? {8'hE9, 8'hB6, 8'h00} :
					//darkblue_bb_active ? {8'h00, 8'h4D, 8'hC0} :
					//pink_bb_active ? {8'hF7, 8'h00, 8'hFF} :
					lightgreen_bb_active ? {8'h22, 8'hFF, 8'h05} :
                    //build_bb_active ? {8'hff, 8'h0, 8'h00} : 
                    //white_bb_active ? {8'h00, 8'h52, 8'hdf} :
                    detected_area;


// Switch output pixels depending on mode switch
// Don't modify the start-of-packet word - it's a packet discriptor
// Don't modify data in non-video packets
assign {red_out, green_out, blue_out} = (mode & ~sop & packet_video) ? new_image : {red,green,blue};
//Count valid pixels to tget the image coordinates. Reset and detect packet type on Start of Packet.
reg [10:0] x, y;

reg [2:0] white_or_black_search; // 2 if searching for white, 1 if for black, 0 if for none yet
reg[3:0] current_number_of_stripes;
reg[3:0] prev_frame_number_of_stripes, frame_1_stripes, frame_2_stripes, frame_3_stripes, max_number_of_stripes;
reg[3:0] non_white_counter;

initial begin
    white_or_black_search = 2;
    max_number_of_stripes = 0;
    current_number_of_stripes = 0;
    prev_frame_number_of_stripes = 0;
    frame_1_stripes = 0;
    frame_2_stripes = 0;
    frame_3_stripes = 0;
    non_white_counter = 0;
end
always @(posedge clk)begin
    if((x==10)&(y==10)&in_valid)begin
        prev_frame_number_of_stripes <= current_number_of_stripes;
        white_or_black_search <= 2;
        current_number_of_stripes <= 0;
    end
    else if((y==230) & (x>=w_x_min) & (x<=w_x_max) & in_valid)begin
        //DO WE NEED BLACK DETECT???/ BOUNDING BOX MADE FROM THE FIRST STRIPE??
        if((white_or_black_search == 2) & white_detect & prev_w1 & prev_w2 & prev_w3 & prev_w4)begin
            current_number_of_stripes <= current_number_of_stripes + 1;
            white_or_black_search <= 1;
            non_white_counter <= 0;
        end
        else if((white_or_black_search == 1))begin
            if(~white_detect & ~prev_w1 & ~prev_w2 & ~prev_w3 & ~prev_w4)begin
                if (non_white_counter >= 2)begin
                    current_number_of_stripes <= current_number_of_stripes + 1;
                    white_or_black_search <= 2;
                end
                else begin
                    non_white_counter <= non_white_counter + 1;
                    white_or_black_search <= 1;
                end    
            end
        end
    end
end

always @(posedge clk) begin
    frame_3_stripes <= frame_2_stripes;
    frame_2_stripes <= frame_1_stripes;
    frame_1_stripes <= prev_frame_number_of_stripes;
    max_number_of_stripes <= (frame_3_stripes > frame_2_stripes) ? ((frame_3_stripes > frame_1_stripes) ? frame_3_stripes : frame_1_stripes) : 
                             (frame_2_stripes > frame_1_stripes) ? ((frame_2_stripes > prev_frame_number_of_stripes) ? frame_2_stripes : prev_frame_number_of_stripes) : 
                             (frame_1_stripes > prev_frame_number_of_stripes) ? frame_1_stripes : prev_frame_number_of_stripes;
end



assign building_detect = (max_number_of_stripes > 3) ? 1 : 0;

reg packet_video;
always@(posedge clk) begin
    if (sop) begin
        red_found <= 0;
        green_found <= 0;
        yellow_found <= 0;
        pink_found <= 0;
        darkblue_found <= 0;
        lightgreen_found <= 0;
        x <= 11'h0;
        y <= 11'h0;
        packet_video <= (blue[3:0] == 3'h0);
    end
    else if (in_valid) begin
        if (red_detect & prev_r1 & prev_r2 & prev_r3 & prev_r4)begin
            red_found <= 1;
        end
        if (green_detect & prev_g1 & prev_g2 & prev_g3 & prev_g4)begin
            green_found <= 1;
        end
        if (yellow_detect & prev_y1 & prev_y2 & prev_y3 & prev_y4)begin
            yellow_found <= 1;
        end
        if (pink_detect & prev_p1 & prev_p2 & prev_p3 & prev_p4)begin
            pink_found <= 1;
        end
        if (darkblue_detect & prev_db1 & prev_db2 & prev_db3 & prev_db4)begin
            darkblue_found <= 1;
        end
        if (lightgreen_detect & prev_lg1 & prev_lg2 & prev_lg3 & prev_lg4)begin
            lightgreen_found <= 1;
        end
        if (x == IMAGE_W-1) begin
            x <= 11'h0;
            y <= y + 11'h1;
        end
        else begin
            x <= x + 11'h1;
        end
    end
end
//Find first and last red pixels for each of the BOUNDING BOXES
//FOR BALLS
//red
reg [10:0] r_x_min, r_y_min, r_x_max, r_y_max;
//green
reg [10:0] g_x_min, g_y_min, g_x_max, g_y_max;
//yellow
reg [10:0] y_x_min, y_y_min, y_x_max, y_y_max;
//darkblue
reg [10:0] db_x_min, db_y_min, db_x_max, db_y_max;
//pink
reg [10:0] p_x_min, p_y_min, p_x_max, p_y_max;
//lightgreen
reg [10:0] lg_x_min, lg_y_min, lg_x_max, lg_y_max;

//FOR BUILDINGS
//black
reg [10:0] b_x_min, b_y_min, b_x_max, b_y_max;
//white
reg [10:0] w_x_min, w_y_min, w_x_max, w_y_max;
//build
reg [10:0] build_x_min, build_y_min, build_x_max, build_y_max;
reg red_ball;
reg [10:0] red_ball_x_min, red_ball_x_max, red_ball_y_min, red_ball_y_max;
always@(posedge clk) begin
    if (red_detect & prev_r1 & prev_r2 & prev_r3 & prev_r4 & in_valid & y > 160) begin
          //Update bounds when the pixel is RED
        if (x < r_x_min) r_x_min <= x;
        if (x > r_x_max) r_x_max <= x;
        if (y < r_y_min) r_y_min <= y;
        r_y_max <= y;
        if((r_width_check < r_height_check + 30) & (r_width_check > r_height_check - 30) & r_in_frame) begin
            red_ball_x_min <= r_x_min;
            red_ball_x_max <= r_x_max;
            red_ball_y_min <= r_y_min;
            red_ball_y_max <= r_y_max;
        end 
    end
    else if (green_detect & prev_g1 & prev_g2 & prev_g3 & prev_g4 & in_valid & y > 160) begin   //Update bounds when the pixel is GREEN
        if (x < g_x_min) g_x_min <= x;
        if (x > g_x_max) g_x_max <= x;
        if (y < g_y_min) g_y_min <= y;
        g_y_max <= y;
    end
    else if (yellow_detect & prev_y1 & prev_y2 & prev_y3 & prev_y4 & in_valid & y > 160) begin    //Update bounds when the pixel is YELLOW
        if (x < y_x_min) y_x_min <= x;
        if (x > y_x_max) y_x_max <= x;
        if (y < y_y_min) y_y_min <= y;
        y_y_max <= y;
    end
    else if (darkblue_detect & prev_db1 & prev_db2 & prev_db3 & prev_db4 & in_valid & y > 160) begin    //Update bounds when the pixel is DARKBLUE
        if (x < y_x_min) y_x_min <= x;
        if (x > y_x_max) y_x_max <= x; 
        if (y < y_y_min) y_y_min <= y;
        y_y_max <= y;
    end
    else if (pink_detect & prev_p1 & prev_p2 & prev_p3 & prev_p4 & in_valid & y > 160) begin    //Update bounds when the pixel is PINK
        if (x < y_x_min) y_x_min <= x;
        if (x > y_x_max) y_x_max <= x;
        if (y < y_y_min) y_y_min <= y;
        y_y_max <= y;
    end
    else if (lightgreen_detect & prev_lg1 & prev_lg2 & prev_lg3 & prev_lg4 & in_valid & y > 160) begin    //Update bounds when the pixel is LIGHT GREEN
        if (x < y_x_min) y_x_min <= x;
        if (x > y_x_max) y_x_max <= x;
        if (y < y_y_min) y_y_min <= y;
        y_y_max <= y;
    end
    else if (black_detect & (x>7) & (x<640-7) & (y>7) & (y < 480-7) & prev_b1 & prev_b2 & prev_b3 & prev_b4 & in_valid & y > 160) begin    //Update bounds when the pixel is BLACK
        if (x < b_x_min) b_x_min <= x;
        if (x > b_x_max) b_x_max <= x;
        if (y < b_y_min) b_y_min <= y;
        b_y_max <= y;
    end
    else if (white_detect & prev_w1 & prev_w2 & prev_w3 & prev_w4 & (x>7) & (x<640-7) & (y>7) & (y < 480-7) & in_valid & y > 160) begin    //Update bounds when the pixel is WHITE
        if (x < w_x_min) begin
            w_x_min <= x;
            if(building_detect) begin
                build_x_min <= x;
            end
        end
        if (x > w_x_max) begin
             w_x_max <= x;
            if(building_detect)begin
                build_x_max <= x;
            end
        end
        if (y < w_y_min) begin
            w_y_min <= y;
            if(building_detect) begin
              build_y_min <= y;
            end
        end
        w_y_max <= y;
        if (building_detect) begin
            build_y_max <= y;
        end 
    end
    // else if (building_detect & (x>7) & (x<640-7) & (y>7) & (y < 480-7) & in_valid) begin    //Update bounds for BUILDING (need to add more logic for black on the side...)
    //     if (x < w_x_min) build_x_min <= x;
    //     if (x > w_x_max) build_x_max <= x;
    //     if (y < w_y_min) build_y_min <= y;
    //     build_y_max <= y;
    // end

    if (sop & in_valid) begin   //Reset bounds on start of packet
        r_x_min <= IMAGE_W-11'h1;
        r_x_max <= 0;
        r_y_min <= IMAGE_H-11'h1;
        r_y_max <= 0;

        g_x_min <= IMAGE_W-11'h1;
        g_x_max <= 0;
        g_y_min <= IMAGE_H-11'h1;
        g_y_max <= 0;

        y_x_min <= IMAGE_W-11'h1;
        y_x_max <= 0;
        y_y_min <= IMAGE_H-11'h1;
        y_y_max <= 0;

        db_x_min <= IMAGE_W-11'h1;
        db_x_max <= 0;
        db_y_min <= IMAGE_H-11'h1;
        db_y_max <= 0;

        p_x_min <= IMAGE_W-11'h1;
        p_x_max <= 0;
        p_y_min <= IMAGE_H-11'h1;
        p_y_max <= 0;

        lg_x_min <= IMAGE_W-11'h1;
        lg_x_max <= 0;
        lg_y_min <= IMAGE_H-11'h1;
        lg_y_max <= 0;

        b_x_min <= IMAGE_W-11'h1;
        b_x_max <= 0;
        b_y_min <= IMAGE_H-11'h1;
        b_y_max <= 0;

        w_x_min <= IMAGE_W-11'h1;
        w_x_max <= 0;
        w_y_min <= IMAGE_H-11'h1;
        w_y_max <= 0;

        build_x_min <= IMAGE_W-11'h1;
        build_x_max <= 0;
        build_y_min <= IMAGE_H-11'h1;
        build_y_max <= 0;
    end
end
//Process bounding box at the end of the frame.
reg [2:0] msg_state;
//defining the left/right/top/bottom for each BOUNDING BOXES for each colour...
//red
reg [10:0] r_left, r_right, r_top, r_bottom;
//green
reg [10:0] g_left, g_right, g_top, g_bottom;
//yellow
reg [10:0] y_left, y_right, y_top, y_bottom;
//darkblue
reg [10:0] db_left, db_right, db_top, db_bottom;
//pink
reg [10:0] p_left, p_right, p_top, p_bottom;
//lightgreen
reg [10:0] lg_left, lg_right, lg_top, lg_bottom;

//BUILDING STUFF
//black
reg [10:0] b_left, b_right, b_top, b_bottom;
//white
reg [10:0] w_left, w_right, w_top, w_bottom;
//BUILDING
reg [10:0] build_left, build_right, build_top, build_bottom;
reg [7:0] frame_count;
always@(posedge clk) begin
    if (eop & in_valid & packet_video) begin  //Ignore non-video packets
        //Latch edges for display overlay on next frame for each BOUNDING BOXES
        //red
        if(red_found)begin
            r_left <= red_ball_x_min;
            r_right <= red_ball_x_max;
            r_top <= red_ball_y_min;
            r_bottom <= red_ball_y_max;
        end
        else begin
            r_left <= 0;
            r_right <= 0;
            r_top <= 0;
            r_bottom <= 0;
        end
        //green
        if(green_found & (g_width_check < g_height_check + 30) & (g_width_check > g_height_check - 30))begin
            g_left <= g_x_min;
            g_right <= g_x_max;
            g_top <= g_y_min;
            g_bottom <= g_y_max;
        end
        // else begin
        //     g_left <= 0;
        //     g_right <= 0;
        //     g_top <= 0;
        //     g_bottom <= 0;
        // end
        
        //yellow
        y_left <= y_x_min;
        y_right <= y_x_max;
        y_top <= y_y_min;
        y_bottom <= y_y_max;
        //darkblue
        db_left <= db_x_min;
        db_right <= db_x_max;
        db_top <= db_y_min;
        db_bottom <= db_y_max;
        //pink
        p_left <= p_x_min;
        p_right <= p_x_max;
        p_top <= p_y_min;
        p_bottom <= p_y_max;
        //lightgreen
        if(lightgreen_found & (lg_width_check < lg_height_check + 30) & (lg_width_check > lg_height_check - 30))begin
            lg_left <= lg_x_min;
            lg_right <= lg_x_max;
            lg_top <= lg_y_min;
            lg_bottom <= lg_y_max;
        end
        // else begin
        //     lg_left <= 0;
        //     lg_right <= 0;
        //     lg_top <= 0;
        //     lg_bottom <= 0;
        // end
        // FOR BUILDINGS
        //black
        b_left <= b_x_min;
        b_right <= b_x_max;
        b_top <= b_y_min;
        b_bottom <= b_y_max;
        //white
        w_left <= w_x_min;
        w_right <= w_x_max;
        w_top <= w_y_min;
        w_bottom <= w_y_max;

        //BUILDINGS
        build_left <= build_x_min;
        build_right <= build_x_max;
        build_top <= build_y_min;
        build_bottom <= build_y_max;
        //Start message writer FSM once every MSG_INTERVAL frames, if there is room in the FIFO
        frame_count <= frame_count - 1;
        if (frame_count == 0 && msg_buf_size < MESSAGE_BUF_MAX - 3) begin
            msg_state <= 3'b001;
            frame_count <= MSG_INTERVAL-1;
        end
    end
    //Cycle through message writer states once started
    if (msg_state != 3'b000) begin
        case(msg_state)
            3'b111: msg_state <= 3'b000;
            default: msg_state <= msg_state + 3'b001;
        endcase
    end
end
//Generate output messages for CPU
reg [31:0] msg_buf_in; 
wire [31:0] msg_buf_out;
reg msg_buf_wr;
wire msg_buf_rd, msg_buf_flush;
wire [7:0] msg_buf_size;
wire msg_buf_empty;
// `define RED_BOX_MSG_ID "RBB"
// `define GREEN_BOX_MSG_ID "GBB"
//msg_buf_in = `RED_BOX_MSG_ID; //Message ID (in the state machine)
//Red ID = 001
//Green ID = 010
//yellow ID = 011
always@(*) begin    //Write words to FIFO as state machine advances
    case(msg_state)
        // 3'b000: begin
		// 	msg_buf_in = 32'b0;
		// 	msg_buf_wr = 1'b0;
		// end
		// 3'b001: begin
		// 	msg_buf_in = {8'b00000001,1'b0,r_x_min,1'b0,r_x_max};	//Red Colour ID, 0-bit + r_x_max, 0-bit + r_x_min
		// 	msg_buf_wr = 1'b1;
		// end
		// 3'b010: begin
		// 	msg_buf_in = {8'b00000001,1'b0,r_y_min,1'b0,r_y_max};	//Red Colour ID, 0-bit + r_x_max, 0-bit + r_x_min
		// 	msg_buf_wr = 1'b1;
		// end
		// 3'b011: begin
		// 	msg_buf_in = {8'b00000010,1'b0,g_x_min,1'b0,g_x_max};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
		// 	msg_buf_wr = 1'b1;
		// end
		// 3'b100: begin
		// 	msg_buf_in = {8'b00000010,1'b0,g_y_min,1'b0,g_y_max};	//pink Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
		// 	msg_buf_wr = 1'b1;
		// end
		// 3'b101: begin
		// 	msg_buf_in = {8'b00000011,1'b0,p_x_min,1'b0,p_x_max};	//pink Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
		// 	msg_buf_wr = 1'b1;
		// end
		// 3'b110: begin
		// 	msg_buf_in = {8'b00000011,1'b0,p_y_min,1'b0,p_y_max};	//pink Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
		// 	msg_buf_wr = 1'b1;
		// end
		3'b000: begin
			msg_buf_in = 32'b0;
			msg_buf_wr = 1'b0;
		end
		3'b001: begin
			msg_buf_in = {31'h1000000, distance_measure_active};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b010: begin
			msg_buf_in = {31'h2000000, r_ball_watching};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b011: begin
			msg_buf_in = {31'h3000000, r_ball_registered};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b100: begin
			msg_buf_in = {16'hFFFF, r_ball_distance};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b101: begin
			msg_buf_in = {16'hAAAA, outbuffer};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b110: begin
			msg_buf_in = {21'h40000, r_width_check};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
        3'b111: begin
			msg_buf_in = {21'h60000, r_height_check};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
    endcase
end
//Output message FIFO
MSG_FIFO    MSG_FIFO_inst (
    .clock (clk),
    .data (msg_buf_in),
    .rdreq (msg_buf_rd),
    .sclr (~reset_n | msg_buf_flush),
    .wrreq (msg_buf_wr),
    .q (msg_buf_out),
    .usedw (msg_buf_size),
    .empty (msg_buf_empty)
    );
//Streaming registers to buffer video signal
STREAM_REG #(.DATA_WIDTH(26)) in_reg (
    .clk(clk),
    .rst_n(reset_n),
    .ready_out(sink_ready),
    .valid_out(in_valid),
    .data_out({red,green,blue,sop,eop}),
    .ready_in(out_ready),
    .valid_in(sink_valid),
    .data_in({sink_data,sink_sop,sink_eop})
);
STREAM_REG #(.DATA_WIDTH(26)) out_reg (
    .clk(clk),
    .rst_n(reset_n),
    .ready_out(out_ready),
    .valid_out(source_valid),
    .data_out({source_data,source_sop,source_eop}),
    .ready_in(source_ready),
    .valid_in(in_valid),
    .data_in({red_out, green_out, blue_out, sop, eop})
);
//RGB->HSV conversion/colour-detection instantiation:
colour_detect detect(
	.hue(hue),
   .sat(sat),
   .val(val),
	.red_detect(red_detect),
	.green_detect(green_detect),
   .yellow_detect(yellow_detect),
   .darkblue_detect(darkblue_detect),
   .pink_detect(pink_detect),
   .lightgreen_detect(lightgreen_detect),
   .black_detect(black_detect),
   .white_detect(white_detect)
);
reg[15:0] r_ball_distance;
reg[15:0] g_ball_distance;
reg[15:0] y_ball_distance; 
reg[15:0] p_ball_distance;
reg[15:0] db_ball_distance; 
reg[15:0] lg_ball_distance;

distance_calc duttt(
    .clk(clk),
    .red_detect(red_detect),
    .r_x_max(r_x_max),
    .r_x_min(r_x_min),
    .green_detect(green_detect),
    .g_x_max(g_x_max),
    .g_x_min(g_x_min),
    .yellow_detect(yellow_detect),
    .y_x_max(y_x_max),
    .y_x_min(y_x_min),
    .pink_detect(pink_detect),
    .p_x_max(p_x_max),
    .p_x_min(p_x_min),
    .darkblue_detect(darkblue_detect),
    .db_x_max(db_x_max),
    .db_x_min(db_x_min),
    .lightgreen_detect(lightgreen_detect),
    .lg_x_max(lg_x_max),
    .lg_x_min(lg_x_min),
    .r_ball_distance(r_ball_distance),
    .g_ball_distance(g_ball_distance),
    .y_ball_distance(y_ball_distance),
    .p_ball_distance(p_ball_distance),
    .db_ball_distance(db_ball_distance),
    .lg_ball_distance(lg_ball_distance),
);



/////////////////////////////////
/// Memory-mapped port       /////
/////////////////////////////////
// Addresses
`define REG_STATUS              0
`define READ_MSG                    1
`define READ_ID                 2
`define REG_BBCOL                   3
//Status register bits
// 31:16 - unimplemented
// 15:8 - number of words in message buffer (read only)
// 7:5 - unused
// 4 - flush message buffer (write only - read as 0)
// 3:0 - unused
// Process write
reg  [7:0]   reg_status;
reg [23:0]  bb_col;
always @ (posedge clk)
begin
    if (~reset_n)
    begin
        reg_status <= 8'b0;
        bb_col <= BB_COL_DEFAULT;
    end
    else begin
        if(s_chipselect & s_write) begin
           if      (s_address == `REG_STATUS)   reg_status <= s_writedata[7:0];
           if      (s_address == `REG_BBCOL)    bb_col <= s_writedata[23:0];
        end
    end
end
//Flush the message buffer if 1 is written to status register bit 4
assign msg_buf_flush = (s_chipselect & s_write & (s_address == `REG_STATUS) & s_writedata[4]);
// Process reads
reg read_d; //Store the read signal for correct updating of the message buffer
// Copy the requested word to the output port when there is a read.
always @ (posedge clk)
begin
   if (~reset_n) begin
       s_readdata <= {32'b0};
        read_d <= 1'b0;
    end
    else if (s_chipselect & s_read) begin
        if   (s_address == `REG_STATUS) s_readdata <= {16'b0,msg_buf_size,reg_status};
        if   (s_address == `READ_MSG) s_readdata <= {msg_buf_out};
        if   (s_address == `READ_ID) s_readdata <= 32'h1234EEE2;
        if   (s_address == `REG_BBCOL) s_readdata <= {8'h0, bb_col};
    end
    read_d <= s_read;
end
//Fetch next word from message buffer after read from READ_MSG
assign msg_buf_rd = s_chipselect & s_read & ~read_d & ~msg_buf_empty & (s_address == `READ_MSG);
endmodule