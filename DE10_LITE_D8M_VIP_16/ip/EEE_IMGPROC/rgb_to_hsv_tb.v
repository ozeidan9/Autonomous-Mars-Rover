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
  r = 22;
  g = 48;
  b = 65;
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
  $display("h is %d, s is %d, v is %d", h,s,v);
  clk = 0;
  r = 235;
  g = 140;
  b = 238;
  #10; 
  clk = ~clk;
  reset = 1;
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
      .clk(clk),
      .rst(reset),
      .rgb_r(r),
      .rgb_g(g),
      .rgb_b(b),
      .hsv_h(h),
      .hsv_s(s),
      .hsv_v(v)
  );

endmodule





