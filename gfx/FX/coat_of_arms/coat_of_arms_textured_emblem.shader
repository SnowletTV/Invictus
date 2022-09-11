Includes = {
	"coat_of_arms/coat_of_arms_textured_emblem.fxh"
}

PixelShader =
{
	MainCode PS_Emblem
	{
		Input = "VS_OUTPUT_COA_ATLAS"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{	
				float4 EmblemTex = PdxTex2D( EmblemMap, Input.uvEmblem );
				
				EmblemTex.r = 0;
				
				float4 EmblemColor = Emblem( Input, EmblemTex );
				
				return EmblemColor;
			}
		]]
	}
	
	MainCode BS_Emblem
	{
		Input = "VS_OUTPUT_COA_ATLAS"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{	
				float4 EmblemTex = PdxTex2D( EmblemMap, Input.uvEmblem );
				
				float4 EmblemColor = Emblem( Input, EmblemTex );
				
				return EmblemColor;
			}
		]]
	}
}

Effect coa_create_textured_emblem
{
	VertexShader = VertexShaderCOAEmblem
	PixelShader = BS_Emblem
	BlendState = BlendState
}

Effect coa_create_textured_emblem_masked
{
	VertexShader = VertexShaderCOAEmblem
	PixelShader = BS_Emblem
	BlendState = BlendState
	Defines = { "USE_PATTERN_MASK" }
}

Effect coa_create_colored_emblem
{
	VertexShader = VertexShaderCOAEmblem
	PixelShader = PS_Emblem
	BlendState = BlendState
	Defines = { "COLORED_EMBLEM" }
}

Effect coa_create_colored_emblem_pattern_mask
{
	VertexShader = VertexShaderCOAEmblem
	PixelShader = PS_Emblem
	BlendState = BlendState
	Defines = { "USE_PATTERN_MASK" "COLORED_EMBLEM" }
}