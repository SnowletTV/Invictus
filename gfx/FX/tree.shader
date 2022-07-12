Includes = {
	"cw/random.fxh" #0 cb
	"cw/utility.fxh" #0 cb
	"constants.fxh" #0 cb
	"standardfuncsgfx.fxh" #1 cb
	"cw/pdxmesh.fxh" #3 cb's (was 5, 1 from camera.fxh)
	"cw/shadow.fxh" #1 cb
	#"cw/camera.fxh" #1 cb (included in pdxmesh.fxh)
	#"cw/heightmap.fxh" #1 cb (included in pdxterrain.fxh)
	"cw/pdxterrain.fxh" #2 cb
	"jomini/jomini_fog.fxh" #1 cb (from jomini.fxh)
	"jomini/jomini_lighting.fxh" #0 cb ( 1 from jomini.fxh, discarded )
	"jomini/jomini_gradient_borders.fxh" #2 cb's (1 from jomini/jomini_colormap_constants.fxh)
	"jomini/jomini_mapobject.fxh" #0 cb
	"fog_of_war.fxh" #2 cb (includes jomini_fog_of_war.fxh which as 1 cb)
	"winter.fxh" #1 cb
}

PixelShader =
{
	TextureSampler DiffuseMap
	{
		Index = 0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler PropertiesMap
	{
		Index = 1
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler NormalMap
	{
		Index = 2
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler EnvironmentMap
	{
		Ref = JominiEnvironmentMap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
		Type = "Cube"
	}
	TextureSampler ShadowTexture
	{
		Ref = PdxShadowmap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
		CompareFunction = less_equal
		SamplerType = "Compare"
	}
	TextureSampler FogOfWarAlpha
	{
		Ref = JominiFogOfWar
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler WinterMap
	{
		Ref = WinterMap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}


	TextureSampler TreeTintMap
	{
		file = "gfx/models/mapitems/trees/tree_tint_01.dds"
		srgb = yes

		Index = 3
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
}

VertexStruct VS_OUTPUT
{
    float4 Position			: PDX_POSITION;
	float3 Normal			: TEXCOORD0;
	float3 Tangent			: TEXCOORD1;
	float3 Bitangent		: TEXCOORD2;
	float2 UV0				: TEXCOORD3;
	float2 UV1				: TEXCOORD4;
	float3 WorldSpacePos	: TEXCOORD5;
	float RandomSeed		: TEXCOORD6;
	uint InstanceIndex 		: TEXCOORD7;
};


VertexShader =
{
	Code
	[[
		struct VS_INPUT
		{
			float3 Position;
			float3 Normal;
			float4 Tangent;
			float2 UV0;
		#ifdef PDX_MESH_UV1
			float2 UV1;
		#endif
		};
		VS_OUTPUT ConvertOutput( in VS_OUTPUT_PDXMESH Output )
		{
			VS_OUTPUT Out;
			Out.Position 		= Output.Position;
			Out.Normal 			= Output.Normal;
			Out.Tangent 		= Output.Tangent;
			Out.Bitangent		= Output.Bitangent;
			Out.UV0				= Output.UV0;
			Out.UV1				= Output.UV1;
			Out.WorldSpacePos 	= Output.WorldSpacePos;
			return Out;
		}

		VS_INPUT ConvertInput( in VS_INPUT_PDXMESHSTANDARD Input )
		{
			VS_INPUT Out;
			Out.Position = Input.Position;
			Out.Normal = Input.Normal;
			Out.Tangent = Input.Tangent;
			Out.UV0 = Input.UV0;
		#ifdef PDX_MESH_UV1
			Out.UV1 = Input.UV1;
		#endif
			return Out;
		}
		VS_INPUT ConvertInput( in VS_INPUT_PDXMESH_MAPOBJECT Input )
		{
			VS_INPUT Out;
			Out.Position = Input.Position;
			Out.Normal = Input.Normal;
			Out.Tangent = Input.Tangent;
			Out.UV0 = Input.UV0;
		#ifdef PDX_MESH_UV1
			Out.UV1 = Input.UV1;
		#endif
			return Out;
		}

		float3 WindTransform( float3 Position, float4x4 WorldMatrix )
		{
			const float NoiseSwayTemporalSpeed = 0.8;
			const float NoiseSwaySpatialSpeed = 0.075;
			const float PhaseSwayTemporalSpeed = 0.5;
			const float PhaseSwaySpatialSpeed = 0.05;
			const float3 SwayWorldDirection = float3(1, 0, 1); //will be normalized
			const float HeightImpactOnSway = 0.33;
			const float SwayScale = 1.1;

			float WorldX = GetMatrixData( WorldMatrix, 0, 3); //Always included
			float WorldY = GetMatrixData( WorldMatrix, 2, 3 );
			float Noise = CalcNoise( GlobalTime * NoiseSwayTemporalSpeed + NoiseSwaySpatialSpeed * float2( WorldX, WorldY ) ); // included: cw/random.fxh
			float Phase = GlobalTime * PhaseSwayTemporalSpeed + PhaseSwaySpatialSpeed * ( WorldX + WorldY );
			float3 Offset = normalize(SwayWorldDirection);
			Offset = mul(Offset, CastTo3x3(WorldMatrix)); //Always included
			float HeightFactor = saturate(Position.y * HeightImpactOnSway);
			HeightFactor *= HeightFactor;
			Position += SwayScale * HeightFactor * sin(Phase) * Offset * Noise * Noise;
			return Position;
		}

		VS_OUTPUT CommonVertexShader( VS_INPUT Input, uint InstanceIndex, float4x4 WorldMatrix )
		{
			VS_OUTPUT Out;

			float4 Position = float4( WindTransform( Input.Position.xyz, WorldMatrix ), 1.0 );

			Out.Normal = normalize( mul( CastTo3x3( WorldMatrix ), Input.Normal ) );
			Out.Tangent = normalize( mul( CastTo3x3( WorldMatrix ), Input.Tangent.xyz ) );
			Out.Bitangent = normalize( cross( Out.Normal, Out.Tangent ) * Input.Tangent.w );

			Out.Position = mul( WorldMatrix, Position );
		#ifdef SNAP_VERTICES_TO_TERRAIN
			Out.Position.y = GetHeight( Out.Position.xz ) + Input.Position.y; // included: cw/heightmap.fxh
		#endif
			Out.WorldSpacePos = Out.Position.xyz;

			Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position ); // included: always

			Out.UV0 = Input.UV0;
		#ifdef PDX_MESH_UV1
			Out.UV1 = Input.UV1;
		#else
			Out.UV1 = vec2( 0.0 );
		#endif
			Out.InstanceIndex = InstanceIndex;
			float4 SeedPos = mul( WorldMatrix, float4(0,0,0,1) );
			Out.RandomSeed = CalcRandom( SeedPos.xz ); // included: cw/random.fxh

			return Out;
		}

		VS_OUTPUT_PDXMESHSHADOW CommonShadowVertexShader( VS_INPUT Input, in float4x4 WorldMatrix )
		{
			VS_OUTPUT_PDXMESHSHADOW Out;
			float4 Position = float4( WindTransform( Input.Position.xyz, WorldMatrix ), 1.0 );
			Out.Position = mul( WorldMatrix, Position );
		#ifdef SNAP_VERTICES_TO_TERRAIN
			Out.Position.y = GetHeight( Out.Position.xz ) + Input.Position.y;
		#endif
			Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );
			Out.UV = Input.UV0;

			return Out;
		}
	]]
	MainCode VS_standard
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT Out = CommonVertexShader( ConvertInput( Input ), Input.InstanceIndices.y, PdxMeshGetWorldMatrix( Input.InstanceIndices.y ) ); // included: cw/pdxmesh.fxh
				return Out;
			}
		]]
	}
	MainCode VS_mapobject
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT Out = CommonVertexShader( ConvertInput( Input ), Input.InstanceIndex24_Opacity8, UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 ) ); // included: jomini/jomini/jomini_mapobject.fxh
				return Out;
			}
		]]
	}
	MainCode VS_shadow
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT_PDXMESHSHADOWSTANDARD"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDXMESHSHADOW Intermediate = CommonShadowVertexShader( ConvertInput( Input ), PdxMeshGetWorldMatrix( Input.InstanceIndices.y ) );
				VS_OUTPUT_PDXMESHSHADOWSTANDARD Out;
				Out.Position = Intermediate.Position;
				Out.UV_InstanceIndex.xy = Intermediate.UV.xy;
				Out.UV_InstanceIndex.z = Input.InstanceIndices.y;
				return Out;
			}
		]]
	}
	MainCode VS_mapobject_shadow
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT_MAPOBJECT_SHADOW"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_MAPOBJECT_SHADOW Out = ConvertOutputMapObjectShadow( CommonShadowVertexShader( ConvertInput( Input ), UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 ) ) );
				Out.InstanceIndex24_Opacity8 = Input.InstanceIndex24_Opacity8;
				return Out;
			}
		]]
	}
}

PixelShader =
{
	Code
	[[
		float GetOpacity( uint InstanceIndex )
		{
			#ifdef JOMINI_MAP_OBJECT
				return UnpackAndGetMapObjectOpacity( InstanceIndex );
			#else
				return PdxMeshGetOpacity( InstanceIndex );
			#endif
		}
	]]
	MainCode PS_standard
	{
		Input = "VS_OUTPUT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float4 Diffuse = PdxTex2D( DiffuseMap, Input.UV0 );
				Diffuse.a = PdxMeshApplyOpacity( Diffuse.a, Input.Position.xy, GetOpacity( Input.InstanceIndex ) );
				clip( Diffuse.a - 0.01 );

				float2 TintUV;
				TintUV.x = Input.UV1.x + Input.RandomSeed;
				TintUV.y = 0.0f;//todo - season

				float4 Properties = PdxTex2D( PropertiesMap, Input.UV0 );

				float3 NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMap, Input.UV0 ) ); // included: cw/utility.fxh

				float3 InNormal = normalize( Input.Normal );
				float3x3 TBN = Create3x3( normalize( Input.Tangent ), normalize( Input.Bitangent ), InNormal );
				float3 Normal = normalize( mul( NormalSample, TBN ) );

				//only leaves (emissive 1.0) should be tinted
				float Emissive =  PdxTex2D( NormalMap, Input.UV0 ).b;
				Diffuse.rgb = lerp( Diffuse.rgb, GetOverlay( Diffuse.rgb, PdxTex2DLod0( TreeTintMap, TintUV ).rgb, 1.0f - Input.UV1.y ), Emissive );

				#if defined( ENABLE_SNOW )
					ApplySnowTree( Diffuse.rgb, Normal, Properties, Input.WorldSpacePos, ColorTexture, WinterMap, DetailTextures, NormalTextures, MaterialTextures ); // included: winter.fxh
				#endif

				float3 BorderColor;
				float BorderPreLightingBlend;
				float BorderPostLightingBlend;
				GetBorderColorAndBlend( Input.WorldSpacePos.xz * WorldSpaceToTerrain0To1, BorderColor, BorderPreLightingBlend, BorderPostLightingBlend ); // included: terrain.fxh
				Diffuse.rgb = lerp( Diffuse.rgb, BorderColor, BorderPreLightingBlend );

				SMaterialProperties MaterialProps = GetMaterialProperties( Diffuse.rgb, Normal, Properties.a, Properties.g, Properties.b ); // included: cw/lighting.fxh
				SLightingProperties LightingProps = GetSunLightingProperties( Input.WorldSpacePos, ShadowTexture ); // included: jomini/jomini_lighting.fxh

				float3 Color = CalculateSunLighting( MaterialProps, LightingProps, EnvironmentMap );

				Color = lerp( Color, BorderColor, BorderPostLightingBlend );

				Color = ApplyFogOfWar( Color, Input.WorldSpacePos, FogOfWarAlpha ); // included :jomini/jomini_fog_of_war.fxh
				Color = ApplyDistanceFog( Color, Input.WorldSpacePos ); // included :jomini/jomini_fog.fxh

				float Alpha = Diffuse.a;

				DebugReturn( Color, MaterialProps, LightingProps, EnvironmentMap ); // included: jomini/jomini_lighting.fxh
				return float4( Color, Alpha );
			}
		]]
	}
}


BlendState BlendState
{
	BlendEnable = no
}

BlendState alpha_to_coverage
{
	#BlendEnable = yes
	#SourceBlend = "SRC_ALPHA"
	#DestBlend = "INV_SRC_ALPHA"
	AlphaToCoverage = yes
}


RasterizerState ShadowRasterizerState
{
	DepthBias = 40000
	SlopeScaleDepthBias = 2
}

DepthStencilState DepthStencilState
{
	StencilEnable = no
	FrontStencilPassOp = replace
	StencilRef = 1
}


Effect tree
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	Defines = { "ENABLE_SNOW" }
}

Effect treeShadow
{
	VertexShader = "VS_shadow"
	PixelShader = "PixelPdxMeshStandardShadow"

	RasterizerState = ShadowRasterizerState
}

Effect tree_alpha_to_coverage
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	BlendState = "alpha_to_coverage"
	Defines = { "ENABLE_SNOW" }
}

Effect tree_alpha_to_coverageShadow
{
	VertexShader = "VS_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	BlendState = "alpha_to_coverage"

	RasterizerState = ShadowRasterizerState
}

Effect tree_cluster
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	Defines = { "SNAP_VERTICES_TO_TERRAIN" "ENABLE_SNOW" }
}
Effect tree_clusterShadow
{
	VertexShader = "VS_shadow"
	PixelShader = "PixelPdxMeshStandardShadow"
	Defines = { "SNAP_VERTICES_TO_TERRAIN" }

	RasterizerState = ShadowRasterizerState
}

Effect tree_cluster_alpha_to_coverage
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	Defines = { "SNAP_VERTICES_TO_TERRAIN" "ENABLE_SNOW" }
	BlendState = "alpha_to_coverage"
}

Effect tree_cluster_alpha_to_coverageShadow
{
	VertexShader = "VS_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	Defines = { "SNAP_VERTICES_TO_TERRAIN" }
	BlendState = "alpha_to_coverage"

	RasterizerState = ShadowRasterizerState
}

############## Map objects ###############

Effect tree_cluster_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	Defines = { "SNAP_VERTICES_TO_TERRAIN" "ENABLE_SNOW" }
}
Effect tree_clusterShadow_mapobject
{
	VertexShader = "VS_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow"

	RasterizerState = ShadowRasterizerState
	Defines = { "SNAP_VERTICES_TO_TERRAIN" }
}

Effect tree_cluster_alpha_to_coverage_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	BlendState = "alpha_to_coverage"
	Defines = { "SNAP_VERTICES_TO_TERRAIN" "ENABLE_SNOW" }
}
Effect tree_cluster_alpha_to_coverageShadow_mapobject
{
	VertexShader = "VS_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow_alphablend"

	RasterizerState = ShadowRasterizerState
	Defines = { "SNAP_VERTICES_TO_TERRAIN" }
}

Effect tree_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	Defines = { "ENABLE_SNOW" }
}
Effect treeShadow_mapobject
{
	VertexShader = "VS_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow"

	RasterizerState = ShadowRasterizerState
}

Effect tree_alpha_to_coverage_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	BlendState = "alpha_to_coverage"
	Defines = { "ENABLE_SNOW" }
}
Effect tree_alpha_to_coverageShadow_mapobject
{
	VertexShader = "VS_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow_alphablend"
	BlendState = "alpha_to_coverage"

	RasterizerState = ShadowRasterizerState
}