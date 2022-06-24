module divider (
	input  clk,
	input [15:0] denominator,
	input [15:0] numerator,
	output [31:0] quotient,
	output [15:0] remainder
);
    reg [31:0] sub_wire0;
    reg [15:0] sub_wire1;
    assign quotient = sub_wire0;
    assign remainder = sub_wire1;

	lpm_divide	LPM_DIVIDE_component (
				.clock (clk),
				.denom (denominator),
				.numer (numerator),
				.quotient (sub_wire0),
				.remain (sub_wire1),
				.aclr (1'b0),
				.clken (1'b1)
	);
	defparam
		LPM_DIVIDE_component.lpm_drepresentation = "UNSIGNED",
		LPM_DIVIDE_component.lpm_hint = "MAXIMIZE_SPEED=6,LPM_REMAINDERPOSITIVE=TRUE",
		LPM_DIVIDE_component.lpm_nrepresentation = "UNSIGNED",
		LPM_DIVIDE_component.lpm_pipeline = 5,
		LPM_DIVIDE_component.lpm_type = "LPM_DIVIDE",
		LPM_DIVIDE_component.lpm_widthd = 16,
		LPM_DIVIDE_component.lpm_widthn = 32;

endmodule