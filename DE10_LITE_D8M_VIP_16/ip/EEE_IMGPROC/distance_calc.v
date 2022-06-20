////////////////////////////////

module distance_calc(
    input clk,
    input red_detect,
    input[10:0] r_x_max,
    input[10:0] r_x_min,
    input green_detect,
    input[10:0] g_x_max,
    input[10:0] g_x_min,
    input yellow_detect,
    input[10:0] y_x_max,
    input[10:0] y_x_min,
    input pink_detect,
    input[10:0] p_x_max,
    input[10:0] p_x_min,
    input darkblue_detect,
    input[10:0] db_x_max,
    input[10:0] db_x_min,
    input lightgreen_detect,
    input[10:0] lg_x_max,
    input[10:0] lg_x_min,
    input building_detect,
    input[10:0] build_left,
    input[10:0] build_right,
    input[10:0] number_of_stripes,
    output reg [15:0]  r_ball_distance,
    output reg[15:0]  g_ball_distance,
    output reg [15:0]  y_ball_distance,
    output reg [15:0]  p_ball_distance,
    output reg[15:0]  db_ball_distance,
    output reg[15:0]  lg_ball_distance,
    output reg[15:0] build_ball_distance
    
);
//WORKING OUT DISTANCES TO OBJECTS



    
wire [10:0] r_ball_center;
wire [10:0] r_ball_width;

wire [10:0] g_ball_center;
wire [10:0] g_ball_width;

wire [10:0] y_ball_center;
wire [10:0] y_ball_width;

wire [10:0] p_ball_center;
wire [10:0] p_ball_width;

wire [10:0] db_ball_center;
wire [10:0] db_ball_width;

wire [10:0] lg_ball_center;
wire [10:0] lg_ball_width;

wire [10:0] building_constant;
wire [10:0] build_ball_center;
wire [10:0] build_ball_width;

assign r_ball_width = r_x_max - r_x_min;
assign r_ball_center = (r_x_max + r_x_min)/2;

assign g_ball_width = g_x_max - g_x_min;
assign g_ball_center = (g_x_max + g_x_min)/2;

assign y_ball_width = y_x_max - y_x_min;
assign y_ball_center = (y_x_max + y_x_min)/2;

assign p_ball_width = p_x_max - p_x_min;
assign p_ball_center = (p_x_max + p_x_min)/2;

assign db_ball_width = db_x_max - db_x_min;
assign db_ball_center = (db_x_max + db_x_min)/2;

assign lg_ball_width = lg_x_max - lg_x_min;
assign lg_ball_center = (lg_x_max + lg_x_min)/2;

assign building_constant = 2839 * number_of_stripes + 1255;
assign build_ball_width = build_right - build_left;
assign build_ball_center = (build_right + build_left)/2;
//RED
always @(posedge clk)begin 
    // if(r_ball_width > 160)begin
    //     r_ball_distance <= 12; //too close
    // end
    // else if(r_ball_width < 50)begin
    //     r_ball_distance <= 11; // too far away
    // end
    if((r_x_max > 320) & (r_x_min < 320) & (r_ball_center < 350) & (r_ball_center > 300))begin
        r_ball_distance[10:0] <= 2550 / r_ball_width;
        r_ball_distance[15:11] <= 1; //COLOUR CODE RED
    end
    else if(r_ball_center > 330)begin
        r_ball_distance <= 10; //too far right
    end
    else begin
        r_ball_distance <= 9; //too far left
    end
end


//GREEN
always @(posedge clk)begin
    // if(g_ball_width > 160)begin
    //     g_ball_distance <= 12; //too close
    // end
    // else if(g_ball_width < 50)begin
    //     g_ball_distance <= 11; // too far away
    // end
    if((g_x_max > 320) & (g_x_min < 320) & (g_ball_center < 340) & (g_ball_center > 300))begin
        g_ball_distance[10:0] <= 2550 / g_ball_width;
        g_ball_distance[15:11] <= 2;
    end
    else if(g_ball_center > 340)begin
        g_ball_distance <= 10; //too far right
    end
    else begin
        g_ball_distance <= 9; //too far left
    end
end

//YELLOW
always @(posedge clk)begin
    if(y_ball_width > 160)begin
        y_ball_distance <= 12; //too close
    end
    else if(y_ball_width < 50)begin
        y_ball_distance <= 11; // too far away
    end
    else if((y_x_max > 320) & (y_x_min < 320) & ( y_ball_center < 330) & (y_ball_center > 310))begin
        y_ball_distance[10:0] <= 2550 / y_ball_width;
        y_ball_distance[15:11] <= 3;
    end
    else if(y_ball_center > 330)begin
        y_ball_distance <= 10; //too far right
    end
    else begin
        y_ball_distance <= 9; //too far left
    end
end

//PINK
always @(posedge clk)begin
    if(p_ball_width > 160)begin
        p_ball_distance <= 12; //too close
    end
    else if(p_ball_width < 50)begin
        p_ball_distance <= 11; // too far away
    end
    else if((p_x_max > 320) & (p_x_min < 320) & ( p_ball_center < 330) & (p_ball_center > 310))begin
        p_ball_distance[10:0] <= 2550 / p_ball_width;
        p_ball_distance[15:11] <= 4;
    end
    else if(p_ball_center > 330)begin
        p_ball_distance <= 10; //too far right
    end
    else begin
        p_ball_distance <= 9; //too far left
    end
end

//DARK BLUE
always @(posedge clk)begin
    if(db_ball_width > 160)begin
        db_ball_distance <= 12; //too close
    end
    else if(db_ball_width < 50)begin
        db_ball_distance <= 11; // too far away
    end
    else if((db_x_max > 320) & (db_x_min < 320) & ( db_ball_center < 330) & (db_ball_center > 310))begin
        db_ball_distance[10:0] <= 2550 / db_ball_width;
        db_ball_distance[15:11] <= 5;
    end
    else if(db_ball_center > 330)begin
        db_ball_distance <= 10; //too far right
    end
    else begin
        db_ball_distance <= 9; //too far left
    end
end

//LIGHT GREEN
always @(posedge clk)begin
    if(lg_ball_width > 160)begin
        lg_ball_distance <= 12; //too close
    end
    else if(lg_ball_width < 50)begin
        lg_ball_distance <= 11; // too far away
    end
    else if((lg_x_max > 320) & (lg_x_min < 320) & ( lg_ball_center < 330) & (lg_ball_center > 310))begin
        lg_ball_distance[10:0] <= 2550 / lg_ball_width;
        lg_ball_distance[15:11] <= 6;
    end
    else if(lg_ball_center > 330)begin
        lg_ball_distance <= 10; //too far right
    end
    else begin
        lg_ball_distance <= 9; //too far left
    end
end





//BUILDINGS 


always @(posedge clk)begin
    if((build_right > 320) & (build_left < 320) & ( build_ball_center < 330) & (build_ball_center > 310))begin
        build_ball_distance[10:0] <= building_constant / build_ball_width;
        build_ball_distance[15:11] <= 7;
    end
    else if(build_ball_center > 330)begin
        build_ball_distance <= 10; //too far right
    end
    else begin
        build_ball_distance <= 9; //too far left
    end
end


endmodule