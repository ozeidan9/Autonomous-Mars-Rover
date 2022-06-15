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
output[15:0]                   outbuffer;
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
reg [15:0] outbuffer_1;
assign outbuffer = outbuffer_1;
//ANthony added
always @(posedge clk)begin
    if(byte_data_received == 1)begin
        if((red_bb_active==1) & (in_valid==1))begin
            outbuffer_1 = 1;
        end else begin
            outbuffer_1 = 1;
        end
    end
    else if (byte_data_received == 2)begin
        //outbuffer_1 = {5'b00000,r_x_min};
        outbuffer_1 = 2;
    end
    else if(byte_data_received == 3)begin
        // outbuffer_1 = {5'b00000,r_x_max};
        outbuffer_1 = 3;
    end
    else if (byte_data_received == 4)begin
        if((green_bb_active==1) & (in_valid==1))begin
            outbuffer_1 = 4;
        end else begin
            outbuffer_1 = 4;
        end
    end
    else if(byte_data_received == 5)begin
        //outbuffer_1 = {5'b00000,g_x_min};
        outbuffer_1 = 5;
    end
    else if(byte_data_received == 6)begin
        // outbuffer_1 = {5'b00000,g_x_max};
        outbuffer_1 = 6;
    end
    else if(byte_data_received == 7)begin
        // outbuffer_1 = 69;
        outbuffer_1 = 7;
    end
end

//end


////////////////////////////////////////////////////////////////////////
// Detect red areas
wire red_detect;
wire green_detect;
wire pink_detect;
// Find boundary of cursor box
reg prev_r1, prev_r2, prev_r3;
reg prev_g1, prev_g2, prev_g3;
reg prev_p1, prev_p2, prev_p3;
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
    prev_g1 <= 0;
    prev_g2 <= 0;
    prev_g3 <= 0;
    prev_p1 <= 0;
    prev_p2 <= 0;
    prev_p3 <= 0;
end
always @(negedge clk)begin
    prev_r3 <= prev_r2;
    prev_r2 <= prev_r1;
    prev_r1 <= red_detect;
    prev_g3 <= prev_g2;
    prev_g2 <= prev_g1;
    prev_g1 <= green_detect;
    prev_p3 <= prev_p2;
    prev_p2 <= prev_p1;
    prev_p1 <= pink_detect;
end
// Highlight detected areas
wire [23:0] detected_area;
assign grey = green[7:1] + red[7:2] + blue[7:2]; //Grey = green/2 + red/4 + blue/4
//changed to black
assign detected_area  =  (red_detect & prev_r1 & prev_r2 & prev_r3) ? {8'hff, 8'h0, 8'h0} : 
                         (green_detect & prev_g1 & prev_g2 & prev_g3) ? {8'h0, 8'hff, 8'h0} :
                         (pink_detect & prev_p1 & prev_p2 & prev_p3) ? {8'h9B, 8'h06, 8'hB8} :
                         {8'h0, 8'h0, 8'h0};
// Show bounding box
wire [23:0] new_image;
//defining the different types of BOUNDING BOXES
wire red_bb_active, green_bb_active, pink_bb_active;
// asssigning the different types of BOUNDING BOXES
//assign red_bb_active = (x == r_left) | (x == r_right) | (y == r_top) | (y == r_bottom);
//assign green_bb_active = (x == g_left) | (x == g_right) | (y == g_top) | (y == g_bottom);
assign red_bb_active = (((x == r_left & r_left != IMAGE_W-11'h1) | (x == r_right & r_right != 0)) & (r_bottom >= y & y >= r_top)) | (((y == r_top) | (y == r_bottom)) & (r_left <= x & x <= r_right));
assign green_bb_active = (((x == g_left & g_left != IMAGE_W-11'h1) | (x == g_right & g_right != 0)) & (g_bottom >= y & y >= g_top)) | (((y == g_top) | (y == g_bottom)) & (g_left <= x & x <= g_right));
assign pink_bb_active = (((x == p_left & p_left != IMAGE_W-11'h1) | (x == p_right & p_right != 0)) & (p_bottom >= y & y >= p_top)) | (((y == p_top) | (y == p_bottom)) & (p_left <= x & x <= p_right));
assign new_image = red_bb_active ? {8'hdf,8'h4d,8'h14} : 
                     green_bb_active ? {8'h97, 8'hdf, 8'h61} :
                     pink_bb_active ? {8'hd7, 8'h08, 8'hff} : 
                     detected_area;
// Switch output pixels depending on mode switch
// Don't modify the start-of-packet word - it's a packet discriptor
// Don't modify data in non-video packets
assign {red_out, green_out, blue_out} = (mode & ~sop & packet_video) ? new_image : {red,green,blue};
//Count valid pixels to tget the image coordinates. Reset and detect packet type on Start of Packet.
reg [10:0] x, y;
reg packet_video;
always@(posedge clk) begin
    if (sop) begin
        x <= 11'h0;
        y <= 11'h0;
        packet_video <= (blue[3:0] == 3'h0);
    end
    else if (in_valid) begin
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
//red
reg [10:0] r_x_min, r_y_min, r_x_max, r_y_max;
//green
reg [10:0] g_x_min, g_y_min, g_x_max, g_y_max;
//pink
reg [10:0] p_x_min, p_y_min, p_x_max, p_y_max;
always@(posedge clk) begin
    if (red_detect & prev_r1 & prev_r2 & prev_r3 & in_valid) begin  //Update bounds when the pixel is RED
        if (x < r_x_min) r_x_min <= x;
        if (x > r_x_max) r_x_max <= x;
        if (y < r_y_min) r_y_min <= y;
        r_y_max <= y;
    end
    else if (green_detect & prev_g1 & prev_g2 & prev_g3 & in_valid) begin   //Update bounds when the pixel is GREEN
        if (x < g_x_min) g_x_min <= x;
        if (x > g_x_max) g_x_max <= x;
        if (y < g_y_min) g_y_min <= y;
        g_y_max <= y;
    end
    else if (pink_detect & prev_p1 & prev_p2 & prev_p3 & in_valid) begin    //Update bounds when the pixel is pink
        if (x < p_x_min) p_x_min <= x;
        if (x > p_x_max) p_x_max <= x;
        if (y < p_y_min) p_y_min <= y;
        p_y_max <= y;
    end
    if (sop & in_valid) begin   //Reset bounds on start of packet
        r_x_min <= IMAGE_W-11'h1;
        r_x_max <= 0;
        r_y_min <= IMAGE_H-11'h1;
        r_y_max <= 0;
        g_x_min <= IMAGE_W-11'h1;
        g_x_max <= 0;
        g_y_min <= IMAGE_H-11'h1;
        g_y_max <= 0;
        p_x_min <= IMAGE_W-11'h1;
        p_x_max <= 0;
        p_y_min <= IMAGE_H-11'h1;
        p_y_max <= 0;
    end
end
//Process bounding box at the end of the frame.
reg [2:0] msg_state;
//defining the left/right/top/bottom for each BOUNDING BOXES for each colour...
//red
reg [10:0] r_left, r_right, r_top, r_bottom;
//green
reg [10:0] g_left, g_right, g_top, g_bottom;
//pink
reg [10:0] p_left, p_right, p_top, p_bottom;
reg [7:0] frame_count;
always@(posedge clk) begin
    if (eop & in_valid & packet_video) begin  //Ignore non-video packets
        //Latch edges for display overlay on next frame for each BOUNDING BOXES
        //red
        r_left <= r_x_min;
        r_right <= r_x_max;
        r_top <= r_y_min;
        r_bottom <= r_y_max;
        //green
        g_left <= g_x_min;
        g_right <= g_x_max;
        g_top <= g_y_min;
        g_bottom <= g_y_max;
        //pink
        p_left <= p_x_min;
        p_right <= p_x_max;
        p_top <= p_y_min;
        p_bottom <= p_y_max;
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
            3'b110: msg_state <= 3'b000;
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
//pink ID = 011
always@(*) begin    //Write words to FIFO as state machine advances
    case(msg_state)
        3'b000: begin
			msg_buf_in = 32'b0;
			msg_buf_wr = 1'b0;
		end
		3'b001: begin
			msg_buf_in = {8'b00000001,1'b0,r_x_min,1'b0,r_x_max};	//Red Colour ID, 0-bit + r_x_max, 0-bit + r_x_min
			msg_buf_wr = 1'b1;
		end
		3'b010: begin
			msg_buf_in = {8'b00000001,1'b0,r_y_min,1'b0,r_y_max};	//Red Colour ID, 0-bit + r_x_max, 0-bit + r_x_min
			msg_buf_wr = 1'b1;
		end
		3'b011: begin
			msg_buf_in = {8'b00000010,1'b0,g_x_min,1'b0,g_x_max};	//Green Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b100: begin
			msg_buf_in = {8'b00000010,1'b0,g_y_min,1'b0,g_y_max};	//pink Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b101: begin
			msg_buf_in = {8'b00000011,1'b0,p_x_min,1'b0,p_x_max};	//pink Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
			msg_buf_wr = 1'b1;
		end
		3'b110: begin
			msg_buf_in = {8'b00000011,1'b0,p_y_min,1'b0,p_y_max};	//pink Colour ID, 0-bit + g_x_max, 0-bit + g_x_min
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
   .pink_detect(pink_detect)
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