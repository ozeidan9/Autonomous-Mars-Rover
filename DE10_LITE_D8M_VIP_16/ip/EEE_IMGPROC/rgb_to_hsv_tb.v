module rgb_to_hsv_tb();
  logic clk;
  logic reset;
  logic[7:0] r,g,b,s,v, cmax, cmin;
  logic [8:0] h;
  


initial begin
  $dumpfile("testing.vcd");
  $dumpvars(0,rgb_to_hsv_tb);
  $display("running");
  clk = 0;
  r = 200;
  g = 50;
  b = 10;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10
  #10; 
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  $display("h is %d, s is %d, v is %d", h,s,v);
  clk = 0;
  r = 235;
  g = 140;
  b = 238;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10;
  $display("h is %d, s is %d, v is %d", h,s,v);
  r = 238;
  g = 14;
  b = 89;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10
  $display("h is %d, s is %d, v is %d", h,s,v);
  r = 35;
  g = 70;
  b = 190;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10;
  clk = ~clk;
  #10; 
  clk = ~clk;
  #10;
  clk = ~clk;
  #10
  $display("h is %d, s is %d, v is %d", h,s,v);


end



  rgb_to_hsv dut(
      .clock(clk),
      .reset(reset),
      .red(r),
      .green(g),
      .blue(b),
      .hue(h),
      .sat(s),
      .val(v)
  );

endmodule





