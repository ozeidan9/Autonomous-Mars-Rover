////////////////////////////////

module distance_calc(
    red_detect,
    r_x_max,
    r_x_min,
    green_detect,
    g_x_max,
    g_x_min,
    yellow_detect,
    y_x_max,
    y_x_min,
    pink_detect,
    p_x_max,
    p_x_min,
    darkblue_detect,
    db_x_max,
    db_x_min,
    lightgreen_detect,
    lg_x_max,
    lg_x_min,
    r_ball_distance,
    g_ball_distance,
    y_ball_distance,
    p_ball_distance,
    db_ball_distance,
    lg_ball_distance
    
)
//WORKING OUT DISTANCES TO OBJECTS

input red_detect, green_detect, yellow_detect, pink_detect, darkblue_detect, lightgreen_detect;
input[10:0] r_x_max, r_x_min, g_x_max, g_x_min, y_x_max, y_x_min, p_x_max, p_x_min, db_x_max, db_x_min, lg_x_max, lg_x_min;
output[10:0] r_ball_distance, g_ball_distance, y_ball_distance, p_ball_distance, db_ball_distance, lg_ball_distance;
    
reg[10:0] r_ball_center;
reg[10:0] r_ball_width;

reg[10:0] g_ball_center;
reg[10:0] g_ball_width;

reg[10:0] y_ball_center;
reg[10:0] y_ball_width;

reg[10:0] p_ball_center;
reg[10:0] p_ball_width;

reg[10:0] db_ball_center;
reg[10:0] db_ball_width;

reg[10:0] lg_ball_center;
reg[10:0] lg_ball_width;



//RED
always @(posedge clk)begin
    if(red_detect)begin
        r_ball_width <= r_x_max - r_x_min;
        r_ball_center <= (r_x_max + r_x_min)/2;
    end
    if(r_ball_width > 160)begin
        r_ball_distance <= 1; //too close
    end
    else if(r_ball_width < 50)begin
        r_ball_distance <= 2; // too far away
    end
    else if((r_x_max > 320) & (r_x_min < 320) & ( r_ball_center < 330) & (r_ball_center > 310))begin
        r_ball_distance <= 2550 / r_ball_width;
    end
    else if(r_ball_center > 330)begin
        r_ball_distance <= 3; //too far right
    end
    else begin
        r_ball_distance <= 4; //too far left
    end
end


//GREEN
always @(posedge clk)begin
    if(green_detect)begin
        g_ball_width <= g_x_max - g_x_min;
        g_ball_center <= (g_x_max + g_x_min)/2;
    end
    if(g_ball_width > 160)begin
        g_ball_distance <= 1; //too close
    end
    else if(g_ball_width < 50)begin
        g_ball_distance <= 2; // too far away
    end
    else if((g_x_max > 320) & (g_x_min < 320) & ( g_ball_center < 330) & (g_ball_center > 310))begin
        g_ball_distance <= 2550 / g_ball_width;
    end
    else if(g_ball_center > 330)begin
        g_ball_distance <= 3; //too far right
    end
    else begin
        g_ball_distance <= 4; //too far left
    end
end

//YELLOW
always @(posedge clk)begin
    if(yellow_detect)begin
        y_ball_width <= y_x_max - y_x_min;
        y_ball_center <= (y_x_max + y_x_min)/2;
    end
    if(y_ball_width > 160)begin
        y_ball_distance <= 1; //too close
    end
    else if(y_ball_width < 50)begin
        y_ball_distance <= 2; // too far away
    end
    else if((y_x_max > 320) & (y_x_min < 320) & ( y_ball_center < 330) & (y_ball_center > 310))begin
        y_ball_distance <= 2550 / y_ball_width;
    end
    else if(y_ball_center > 330)begin
        y_ball_distance <= 3; //too far right
    end
    else begin
        y_ball_distance <= 4; //too far left
    end
end

//PINK
always @(posedge clk)begin
    if(pink_detect)begin
        p_ball_width <= p_x_max - p_x_min;
        p_ball_center <= (p_x_max + p_x_min)/2;
    end
    if(p_ball_width > 160)begin
        p_ball_distance <= 1; //too close
    end
    else if(p_ball_width < 50)begin
        p_ball_distance <= 2; // too far away
    end
    else if((p_x_max > 320) & (p_x_min < 320) & ( p_ball_center < 330) & (p_ball_center > 310))begin
        p_ball_distance <= 2550 / p_ball_width;
    end
    else if(p_ball_center > 330)begin
        p_ball_distance <= 3; //too far right
    end
    else begin
        p_ball_distance <= 4; //too far left
    end
end

//DARK BLUE
always @(posedge clk)begin
    if(darkblue_detect)begin
        db_ball_width <= db_x_max - db_x_min;
        db_ball_center <= (db_x_max + db_x_min)/2;
    end
    if(db_ball_width > 160)begin
        db_ball_distance <= 1; //too close
    end
    else if(db_ball_width < 50)begin
        db_ball_distance <= 2; // too far away
    end
    else if((db_x_max > 320) & (db_x_min < 320) & ( db_ball_center < 330) & (db_ball_center > 310))begin
        db_ball_distance <= 2550 / db_ball_width;
    end
    else if(db_ball_center > 330)begin
        db_ball_distance <= 3; //too far right
    end
    else begin
        db_ball_distance <= 4; //too far left
    end
end

//LIGHT GREEN
always @(posedge clk)begin
    if(lightgreen_detect)begin
        lg_ball_width <= lg_x_max - lg_x_min;
        lg_ball_center <= (lg_x_max + lg_x_min)/2;
    end
    if(lg_ball_width > 160)begin
        lg_ball_distance <= 1; //too close
    end
    else if(lg_ball_width < 50)begin
        lg_ball_distance <= 2; // too far away
    end
    else if((lg_x_max > 320) & (lg_x_min < 320) & ( lg_ball_center < 330) & (lg_ball_center > 310))begin
        lg_ball_distance <= 2550 / lg_ball_width;
    end
    else if(lg_ball_center > 330)begin
        lg_ball_distance <= 3; //too far right
    end
    else begin
        lg_ball_distance <= 4; //too far left
    end
end
endmodule