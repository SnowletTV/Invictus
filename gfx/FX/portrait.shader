Includes = {
	"cw/pdxmesh.fxh"
	"cw/pdxmesh_blendshapes.fxh"
	"cw/utility.fxh"
	"cw/shadow.fxh"
	"cw/camera.fxh"
	"cw/random.fxh"
	"jomini/jomini_lighting.fxh"
	"jomini/jomini_fog.fxh"
	"constants.fxh"
	"standardfuncsgfx.fxh"
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
	TextureSampler SpecularMap
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
	TextureSampler SkinDecalDiffuseAtlas
	{
		Index = 5
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler SkinDecalNormalAtlas
	{
		Index = 6
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler PaintDecalDiffuseAtlas
	{
		Index = 7
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler PaintDecalPropertyAtlas
	{
		Index = 8
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler DecalData
	{
		Index = 9
		MagFilter = "point"
		MinFilter = "point"
		MipFilter = "point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler DiffuseMapOverride
	{
		Index = 10
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler NormalMapOverride
	{
		Index = 11
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler SpecularMapOverride
	{
		Index = 12
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
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
}

VertexShader = {
	TextureSampler BlendShapeTexture
	{
		Index = 15
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
}


VertexStruct VS_OUTPUT_PDXMESHPORTRAIT
{
    float4 	Position		: PDX_POSITION;
	float3 	Normal			: TEXCOORD0;
	float3 	Tangent			: TEXCOORD1;
	float3 	Bitangent		: TEXCOORD2;
	float2 	UV0				: TEXCOORD3;
	float2 	UV1				: TEXCOORD4;
	float3 	WorldSpacePos	: TEXCOORD5;
	float4 	ShadowProj		: TEXCOORD6;
	uint 	InstanceIndex	: TEXCOORD7;
};

VertexStruct VS_INPUT_PDXMESHSTANDARD_ID
{
    float3 Position			: POSITION;
	float3 Normal      		: TEXCOORD0;
	float4 Tangent			: TEXCOORD1;
	float2 UV0				: TEXCOORD2;
@ifdef PDX_MESH_UV1     	
	float2 UV1				: TEXCOORD3;
@endif

	uint2 InstanceIndices 	: TEXCOORD4;
	
@ifdef PDX_MESH_SKINNED
	uint4 BoneIndex 		: TEXCOORD5;
	float3 BoneWeight		: TEXCOORD6;
@endif

	uint VertexID			: PDX_VertexID;
};

# Portrait constants
ConstantBuffer( 5 )
{
	float4 		vPaletteColorSkin;
	float4 		vPaletteColorEyes;
	float4 		vPaletteColorHair;
	float4		vSkinPropertyMult;
	float4		vEyesPropertyMult;
	float4		vHairPropertyMult;
	
	float4 		Light_Color_Falloff[3];
	float4 		Light_Position_Radius[3]
	float4 		Light_Direction_Type[3];
	float4 		Light_InnerCone_OuterCone_AffectedByShadows[3];
	
	int2		nDecalCount;
	float		PortraitDecalAtlasSize;
	float		TextureOverride;
};
Code
[[
	#define LIGHT_COUNT 3
	#define LIGHT_TYPE_NONE 0
	#define LIGHT_TYPE_DIRECTIONAL 1
	#define LIGHT_TYPE_SPOTLIGHT 2
	#define LIGHT_TYPE_POINTLIGHT 3
]]

VertexShader = {

	Code
	[[
		VS_OUTPUT_PDXMESHPORTRAIT ConvertOutput( VS_OUTPUT_PDXMESH In )
		{
			VS_OUTPUT_PDXMESHPORTRAIT Out;
			
			Out.Position = In.Position;
			Out.Normal = In.Normal;
			Out.Tangent = In.Tangent;
			Out.Bitangent = In.Bitangent;
			Out.UV0 = In.UV0;
			Out.UV1 = In.UV1;
			Out.WorldSpacePos = In.WorldSpacePos;
			Out.ShadowProj = mul( ShadowMapTextureMatrix, float4( Out.WorldSpacePos, 1.0 ) );
			return Out;
		}
		
		void ProcessBlendShapes( out float3 PosDiff, out float3 NormalDiff, out float4 TangentDiff, in int nVertIndex )
		{
			PosDiff = float3(0.0, 0.0, 0.0);
			NormalDiff = float3(0.0, 0.0, 0.0);
			TangentDiff = float4(0.0, 0.0, 0.0, 0.0);
			int nVector = 0, nElement = 0;
			for ( int i = 0; i < int( nActiveBlendShapes ); ++i )
			{
				int nRow = int( blendShapeIndices[nVector][nElement] ) * 3;
				float vWeight = blendShapeWeights[nVector][nElement];
				PosDiff += PdxTex2DLoad0( BlendShapeTexture, int2(nVertIndex, nRow) ).xyz * vWeight;
				++nRow;
				NormalDiff += PdxTex2DLoad0( BlendShapeTexture, int2(nVertIndex, nRow) ).xyz * vWeight;
				++nRow;
				TangentDiff += PdxTex2DLoad0( BlendShapeTexture, int2(nVertIndex, nRow) ).xyzw * vWeight;
				++nRow;
				++nElement;
				if (nElement == 4)
				{
					nElement = 0;
					++nVector;
				}
			}
		}
		
		void ProcessBlendShapesPositionOnly( out float3 PosDiff, in int nVertIndex )
		{
			PosDiff = float3(0.0, 0.0, 0.0);
			int nVector = 0, nElement = 0;
			for ( int i = 0; i < int( nActiveBlendShapes ); ++i )
			{
				int nRow = int( blendShapeIndices[nVector][nElement] ) * 3;
				float vWeight = blendShapeWeights[nVector][nElement];
				PosDiff += PdxTex2DLoad0( BlendShapeTexture, int2(nVertIndex, nRow) ).xyz * vWeight;
				++nElement;
				if (nElement == 4)
				{
					nElement = 0;
					++nVector;
				}
			}
		}
	]]
	
	MainCode VS_portrait_blend_shapes
	{
		Input = "VS_INPUT_PDXMESHSTANDARD_ID"
		Output = "VS_OUTPUT_PDXMESHPORTRAIT"
		Code
		[[
			PDX_MAIN
			{
			  	VS_OUTPUT_PDXMESHPORTRAIT Out;
				
				float4 vPosition = float4( Input.Position.xyz, 1.0f );
				float3 vBlendPositionDiff, vBlendNormalDiff;
				float4 vBlendTangentDiff;
				int nVertIndex = int( nBlendShapesVertexOffset ) + int( Input.VertexID );
				ProcessBlendShapes( vBlendPositionDiff, vBlendNormalDiff, vBlendTangentDiff, nVertIndex );
				vPosition.xyz += vBlendPositionDiff;
				
				float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );
			#ifdef PDX_MESH_SKINNED
				float4 vSkinnedPosition = float4( 0, 0, 0, 0 );
				float3 vSkinnedNormal = float3( 0, 0, 0 );
				float3 vSkinnedTangent = float3( 0, 0, 0 );
				float3 vSkinnedBitangent = float3( 0, 0, 0 );
			
				float4 vWeight = float4( Input.BoneWeight.xyz, 1.0f - Input.BoneWeight.x - Input.BoneWeight.y - Input.BoneWeight.z );
			
				for( int i = 0; i < PDXMESH_MAX_INFLUENCE; ++i )
			    {
					int nIndex = int( Input.BoneIndex[i] );
					float4x4 mat = BoneMatrices[nIndex + Input.InstanceIndices.x];
					vSkinnedPosition += mul( mat, vPosition ) * vWeight[i];
			
					float3 vNormal = mul( CastTo3x3(mat), Input.Normal + vBlendNormalDiff );
					float3 vTangent = mul( CastTo3x3(mat), Input.Tangent.xyz + vBlendTangentDiff.xyz );
					float3 vBitangent = cross( vNormal, vTangent ) * (Input.Tangent.w + vBlendTangentDiff.w);
			
					vSkinnedNormal += vNormal * vWeight[i];
					vSkinnedTangent += vTangent * vWeight[i];
					vSkinnedBitangent += vBitangent * vWeight[i];
				}
			
				Out.Position = mul( WorldMatrix, vSkinnedPosition );
				
				Out.Normal = normalize( mul( CastTo3x3(WorldMatrix), normalize( vSkinnedNormal ) ) );
				Out.Tangent = normalize( mul( CastTo3x3(WorldMatrix), normalize( vSkinnedTangent ) ) );
				Out.Bitangent = normalize( mul( CastTo3x3(WorldMatrix), normalize( vSkinnedBitangent ) ) );
			#else
				Out.Position = mul( WorldMatrix, vPosition );
				
				Out.Normal = normalize( mul( CastTo3x3( WorldMatrix ), Input.Normal + vBlendNormalDiff ) );
				Out.Tangent = normalize( mul( CastTo3x3( WorldMatrix ), Input.Tangent.xyz + vBlendTangentDiff.xyz ) );
				Out.Bitangent = normalize( cross( Out.Normal, Out.Tangent ) * (Input.Tangent.w + vBlendTangentDiff.w) );
			#endif
			
				Out.WorldSpacePos.xyz = Out.Position.xyz;
				Out.WorldSpacePos /= WorldMatrix[3][3];
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );
				
				Out.ShadowProj = mul( ShadowMapTextureMatrix, float4( Out.WorldSpacePos, 1.0 ) );
				
				Out.UV0 = Input.UV0;
			#ifdef PDX_MESH_UV1
				Out.UV1 = Input.UV1;
			#else
				Out.UV1 = vec2( 0.0 );
			#endif
				Out.InstanceIndex = Input.InstanceIndices.y;
				return Out;
			}
		]]
	}

	MainCode VS_portrait_blend_shapes_shadow
	{
		Input = "VS_INPUT_PDXMESHSTANDARD_ID"
		Output = "VS_OUTPUT_PDXMESHSHADOWSTANDARD"
		Code
		[[
			PDX_MAIN
			{
			  	VS_OUTPUT_PDXMESHSHADOWSTANDARD Out;
				
				float4 vPosition = float4( Input.Position.xyz, 1.0 );
				float3 vBlendPositionDiff;
				int nVertIndex = int( nBlendShapesVertexOffset ) + int( Input.VertexID );
				ProcessBlendShapesPositionOnly( vBlendPositionDiff, nVertIndex );
				vPosition.xyz += vBlendPositionDiff;
				
				float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );
			#ifdef PDX_MESH_SKINNED
				float4 vSkinnedPosition = float4( 0, 0, 0, 0 );
			
				float4 vWeight = float4( Input.BoneWeight.xyz, 1.0f - Input.BoneWeight.x - Input.BoneWeight.y - Input.BoneWeight.z );
				for( int i = 0; i < PDXMESH_MAX_INFLUENCE; ++i )
			    {
					int nIndex = int( Input.BoneIndex[i] );
					float4x4 mat = BoneMatrices[nIndex + Input.InstanceIndices.x];
					vSkinnedPosition += mul( mat, vPosition ) * vWeight[i];
				}
				Out.Position = mul( WorldMatrix, vSkinnedPosition );
			#else
				Out.Position = mul( WorldMatrix, vPosition );
			#endif
			
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );
				Out.UV_InstanceIndex = float3( Input.UV0, Input.InstanceIndices.y );
				return Out;
			}
		]]
	}
	
	MainCode VS_standard
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT_PDXMESHPORTRAIT"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDXMESHPORTRAIT Out = ConvertOutput( PdxMeshVertexShaderStandard( Input ) );
				Out.InstanceIndex = Input.InstanceIndices.y;
				return Out;
			}
		]]
	}
}

PixelShader =
{
	Code
	[[		
		void CalculatePortraitLights( float3 WorldSpacePos, float ShadowTerm, SMaterialProperties MaterialProps, inout float3 DiffuseLightOut, inout float3 SpecularLightOut )
		{
			for( int i = 0; i < LIGHT_COUNT; ++i )
			{
				float3 DiffuseLight = vec3(0);
				float3 SpecularLight = vec3(0);
				
				//Scale color by ShadowTerm
				float4 Color_Fallof = Light_Color_Falloff[i];
				float LightShadowTerm = Light_InnerCone_OuterCone_AffectedByShadows[i].z > 0.5 ? ShadowTerm : 1.0;
				
				if( Light_Direction_Type[i].w == LIGHT_TYPE_SPOTLIGHT )
				{
					float InnerAngle = Light_InnerCone_OuterCone_AffectedByShadows[i].x;
					float OuterAngle = Light_InnerCone_OuterCone_AffectedByShadows[i].y;
					SpotLight Spot = GetSpotLight( Light_Position_Radius[i], Color_Fallof, Light_Direction_Type[i].xyz, InnerAngle, OuterAngle );
					GGXSpotLight( Spot, WorldSpacePos, LightShadowTerm, MaterialProps, DiffuseLight, SpecularLight );
				}
				else if( Light_Direction_Type[i].w == LIGHT_TYPE_POINTLIGHT )
				{
					PointLight Light = GetPointLight( Light_Position_Radius[i], Color_Fallof );
					GGXPointLight( Light, WorldSpacePos, LightShadowTerm, MaterialProps, DiffuseLight, SpecularLight );
				}
				else if( Light_Direction_Type[i].w == LIGHT_TYPE_DIRECTIONAL )
				{
					SLightingProperties LightingProps;
					LightingProps._ToCameraDir = normalize( CameraPosition - WorldSpacePos );
					LightingProps._ToLightDir = -Light_Direction_Type[i].xyz;
					LightingProps._LightIntensity = Color_Fallof.rgb;
					LightingProps._ShadowTerm = LightShadowTerm;
					LightingProps._CubemapIntensity = 0.0;
					CalculateLightingFromLight( MaterialProps, LightingProps, DiffuseLight, SpecularLight );
				}
				
				DiffuseLightOut += DiffuseLight;
				SpecularLightOut += SpecularLight;
			}
		}
		
		void DebugReturn( inout float3 Out, SMaterialProperties MaterialProps, SLightingProperties LightingProps, PdxTextureSamplerCube EnvironmentMap, float3 SssColor, float SssMask )
		{
			#if defined(PDX_DEBUG_PORTRAIT_SSS_MASK)
			Out = SssMask;
			#elif defined(PDX_DEBUG_PORTRAIT_SSS_COLOR)
			Out = SssColor;
			#else
			DebugReturn( Out, MaterialProps, LightingProps, EnvironmentMap );
			#endif
		}

		float3 CommonPixelShader( float4 Diffuse, float4 Properties, float3 NormalSample, in VS_OUTPUT_PDXMESHPORTRAIT Input )
		{
			float3x3 TBN = Create3x3( normalize( Input.Tangent ), normalize( Input.Bitangent ), normalize( Input.Normal ) );
			float3 Normal = normalize( mul( NormalSample, TBN ) );
			
			SMaterialProperties MaterialProps = GetMaterialProperties( Diffuse.rgb, Normal, saturate( Properties.a ), Properties.g, Properties.b );
			SLightingProperties LightingProps = GetSunLightingProperties( Input.WorldSpacePos, ShadowTexture );
			
			float3 DiffuseIBL;
			float3 SpecularIBL;
			CalculateLightingFromIBL( MaterialProps, LightingProps, EnvironmentMap, DiffuseIBL, SpecularIBL );
			
			float3 DiffuseLight = vec3(0.0);
			float3 SpecularLight = vec3(0.0);
			CalculatePortraitLights( Input.WorldSpacePos, LightingProps._ShadowTerm, MaterialProps, DiffuseLight, SpecularLight );
			
			float3 Color = DiffuseIBL + SpecularIBL + DiffuseLight + SpecularLight;
			
			float3 SssColor = vec3(0.0f);
			float SssMask = Properties.r;
			#ifdef FAKE_SSS_EMISSIVE
				float3 SkinColor = RGBtoHSV( Diffuse.rgb );
				SkinColor.z = 1.0f;
				SssColor = HSVtoRGB(SkinColor) * SssMask * 0.5f * MaterialProps._DiffuseColor;
				Color += SssColor;
			#endif
			
			Color = ApplyDistanceFog( Color, Input.WorldSpacePos );
			
			DebugReturn( Color, MaterialProps, LightingProps, EnvironmentMap, SssColor, SssMask );			
			return Color;
		}
		
		// MOD
		float4 get_attatchment_color(in VS_OUTPUT_PDXMESHPORTRAIT Input, float3 VariationColor)
		{
			float2 UV0 = Input.UV0;
			float4 Diffuse = PdxTex2D( DiffuseMap, UV0 );								

			float SaturationThreshold = 0.05;

			float MinColor = min(min(Diffuse.r, Diffuse.g), Diffuse.b);
			float MaxColor = max(max(Diffuse.r, Diffuse.g), Diffuse.b);
			float Saturation = MaxColor - MinColor;
			if (Saturation < SaturationThreshold)
			{
				Diffuse.rgb *= VariationColor;
			}

			float4 Properties = PdxTex2D( SpecularMap, UV0 );
			float3 NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMap, UV0 ) );			
			float3 Color = CommonPixelShader( Diffuse, Properties, NormalSample, Input );			
			return float4( Color, Diffuse.a );
		}
		// END MOD
	]]

	MainCode PS_skin
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			float3 UnpackDecalNormal( float4 NormalSample, float DecalStrength )
			{
				float3 Normal;
				//Sample format is RRxG
				Normal.xy = NormalSample.ga * 2.0 - vec2(1.0);
				Normal.y = -Normal.y;
				
				//Filter out "weak" normals. Compression/precision errors will scale with the number of decals used, so try to remove errors where artists intended the normals to be neutral
				float NormalXYSquared = dot( Normal.xy, Normal.xy );
				const float FilterMin = 0.0004f;
				const float FilterWidth = 0.05f;
				float Filter = smoothstep( FilterMin, FilterMin+FilterWidth*FilterWidth, NormalXYSquared );
				
				Normal.xy *= DecalStrength * Filter;
				Normal.z = sqrt( saturate( 1.0 - dot(Normal.xy,Normal.xy) ) );
				return Normal;
			}
			void AddSkinDecals( inout float3 Diffuse, inout float3 Normals, float2 UV )
			{
				float PortraitMaxDecals = PortraitDecalAtlasSize*PortraitDecalAtlasSize;
				float vDiffuseTotal = 0.0f;
				float3 DecalDiffuse = vec3( 0.0f );
				for( int i = 0; i < nDecalCount.x; ++i )
				{
					float3 Data = PdxTex2DLod0( DecalData, float2( i / PortraitMaxDecals, 0.0f ) ).xyz;
					float2 DecalUV = ( Data.xy * 255.0f + UV ) / PortraitDecalAtlasSize;
					
					float4 DiffuseSample = PdxTex2D( SkinDecalDiffuseAtlas, DecalUV );
					float3 NormalSample = UnpackDecalNormal( PdxTex2D( SkinDecalNormalAtlas, DecalUV ), Data.z );

					float vWeight = DiffuseSample.a * Data.z;
					DecalDiffuse += DiffuseSample.rgb * vWeight;
					vDiffuseTotal += vWeight;					
					
					Normals.xy += NormalSample.xy;
					Normals.z *= NormalSample.z;
				}
				DecalDiffuse /= max( 0.001f, vDiffuseTotal );
				Diffuse = lerp( Diffuse, Overlay( Diffuse, DecalDiffuse ), min( vDiffuseTotal, 1.0f ) );
				Normals = normalize( Normals );
			}
			
			void AddPaintDecals( inout float3 Diffuse, inout float4 Properties, float2 UV )
			{
				float PortraitMaxDecals = PortraitDecalAtlasSize*PortraitDecalAtlasSize;
				float vDiffuseTotal = 0.0f;
				float3 DecalDiffuse = vec3( 0.0f );
				float4 DecalProperties = vec4( 0.0f );
				for( int i = 0; i < nDecalCount.y; ++i )
				{
					float3 Data = PdxTex2D( DecalData, float2( i / PortraitMaxDecals, 1.0f ) ).xyz;
					float2 DecalUV = ( Data.xy * 255.0f + UV ) / PortraitDecalAtlasSize;
					
					float4 DiffuseSample = PdxTex2D( PaintDecalDiffuseAtlas, DecalUV );
					float4 PropertySample = PdxTex2D( PaintDecalPropertyAtlas, DecalUV );

					float vWeight = DiffuseSample.a * Data.z;
					vDiffuseTotal += vWeight;
					DecalDiffuse += DiffuseSample.rgb * vWeight;
					DecalProperties += PropertySample * vWeight;
				}
				if( vDiffuseTotal > 1.0f )
				{
					DecalDiffuse /= vDiffuseTotal;
					DecalProperties /= vDiffuseTotal;
					vDiffuseTotal = 1.0f;
				}
				float vAlpha = smoothstep( 0.5, 1.0, vDiffuseTotal );
				Diffuse = lerp( Diffuse, DecalDiffuse, vAlpha );
				Properties = lerp( Properties, DecalProperties, vAlpha );
			}
		
			PDX_MAIN
			{			
				float2 UV0 = Input.UV0;
				float4 Diffuse;
				float4 Properties;
				float3 NormalSample;
			#ifdef ENABLE_TEXTURE_OVERRIDE
				if( TextureOverride > 0.5f )
				{
					Diffuse = PdxTex2D( DiffuseMapOverride, UV0 );
					Properties = PdxTex2D( SpecularMapOverride, UV0 );
					NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMapOverride, UV0 ) );
				}
				else
			#endif
				{
					Diffuse = PdxTex2D( DiffuseMap, UV0 );						
					Properties = PdxTex2D( SpecularMap, UV0 );
					NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMap, UV0 ) );
				}

				// Add skin decals first, then apply skin color, and then paint decals
			#ifdef ENABLE_DECALS
				AddSkinDecals( Diffuse.rgb, NormalSample, UV0 );
			#endif				
				Diffuse.rgb = lerp( Diffuse.rgb, Diffuse.rgb * vPaletteColorSkin.rgb, Diffuse.a );
			#ifdef ENABLE_DECALS
				AddPaintDecals( Diffuse.rgb, Properties, UV0 );
			#endif
				
				float3 Color = CommonPixelShader( Diffuse, Properties, NormalSample, Input );
				
				return float4( Color, 1.0f );
			}
			
		]]
	}
	
	MainCode PS_eye
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float2 UV0 = Input.UV0;
				float4 Diffuse = PdxTex2D( DiffuseMap, UV0 );								
				float4 Properties = PdxTex2D( SpecularMap, UV0 );
				float3 NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMap, UV0 ) );
				
				Diffuse.rgb = lerp( Diffuse.rgb, Diffuse.rgb * vPaletteColorEyes.rgb, Diffuse.a );
				
				float3 Color = CommonPixelShader( Diffuse, Properties, NormalSample, Input );
				
				return float4( Color, 1.0f );
			}
		]]
	}

	MainCode PS_attachment
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float2 UV0 = Input.UV0;
				float4 Diffuse = PdxTex2D( DiffuseMap, UV0 );								
				float4 Properties = PdxTex2D( SpecularMap, UV0 );
				float3 NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMap, UV0 ) );			
				float3 Color = CommonPixelShader( Diffuse, Properties, NormalSample, Input );			
				return float4( Color, Diffuse.a );
			}
		]]
	}

	#MOD
	MainCode PS_attachment_variation_red
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.627, 0.117, 0.117);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_white
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.853, 0.828, 0.746);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_yellow
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.9, 0.69, 0.302);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_gold
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.649, 0.418, 0.09);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_brown
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.522, 0.412, 0.337);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_grey
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.425, 0.425, 0.44);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_orange
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.871, 0.416, 0.133);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_blue
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.243, 0.357, 0.459);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_green
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.42, 0.565, 0.38);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	MainCode PS_attachment_variation_dark_green
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float3 VariationColor = float3(0.278, 0.349, 0.259);
				return get_attatchment_color(Input, VariationColor);
			}
		]]
	}
	#END MOD

	MainCode PS_portrait_hair_backface
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{			
				return float4( vec3( 0.0f ), 1.0f );
			}
		]]
	}
	MainCode PS_hair
	{
		Input = "VS_OUTPUT_PDXMESHPORTRAIT"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{			
				float2 UV0 = Input.UV0;
				float4 Diffuse = PdxTex2D( DiffuseMap, UV0 );		
				clip( Diffuse.a - 0.5f );
				float4 Properties = PdxTex2D( SpecularMap, UV0 );
				float3 NormalSample = UnpackRRxGNormal( PdxTex2D( NormalMap, UV0 ) );
				
				Properties *= vHairPropertyMult;
				Diffuse.rgb *= vPaletteColorHair.rgb;
				
				float3 Color = CommonPixelShader( Diffuse, Properties, NormalSample, Input );
				return float4( Color, Diffuse.a );
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
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
	WriteMask = "RED|GREEN|BLUE|ALPHA"
	SourceAlpha = "ONE"
	DestAlpha = "INV_SRC_ALPHA"
	#BlendOpAlpha = "max"
	AlphaToCoverage = yes
}

BlendState alpha_blend
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
	WriteMask = "RED|GREEN|BLUE|ALPHA"
	BlendOpAlpha = "max"
	AlphaToCoverage = no
}

DepthStencilState test_and_write
{
	DepthEnable = yes
	DepthWriteEnable = yes
}
DepthStencilState test_no_write
{
	DepthEnable = yes
	DepthWriteEnable = no
}


RasterizerState rasterizer_backfaces
{
	FrontCCW = yes
}
RasterizerState rasterizer_no_culling
{
	CullMode = "none"
}
RasterizerState ShadowRasterizerState
{
	DepthBias = 70000
	SlopeScaleDepthBias = 2
}
RasterizerState ShadowRasterizerStateBackfaces
{
	DepthBias = 100000
	SlopeScaleDepthBias = 2
	FrontCCW = yes
}



Effect portrait_skin
{
	VertexShader = "VS_portrait_blend_shapes"
	PixelShader = "PS_skin"
	Defines = { "FAKE_SSS_EMISSIVE" }
}
Effect portrait_skinShadow
{
	VertexShader = "VS_portrait_blend_shapes_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
}
Effect portrait_skin_face
{
	VertexShader = "VS_portrait_blend_shapes"
	PixelShader = "PS_skin"
	Defines = { "FAKE_SSS_EMISSIVE" "ENABLE_DECALS" "ENABLE_TEXTURE_OVERRIDE" }
}
Effect portrait_skin_faceShadow
{
	VertexShader = "VS_portrait_blend_shapes_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
}


Effect portrait_eye
{
	VertexShader = "VS_standard"
	PixelShader = "PS_eye"
}
Effect portrait_eyeShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
}

# MOD
Effect pav_red
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_red"
}
Effect pav_redShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_white
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_white"
}
Effect pav_whiteShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_yellow
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_yellow"
}
Effect pav_yellowShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_gold
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_gold"
}
Effect pav_goldShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_brown
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_brown"
}
Effect pav_brownShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_grey
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_grey"
}
Effect pav_greyShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_orange
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_orange"
}
Effect pav_orangeShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_blue
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_blue"
}
Effect pav_blueShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_green
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_green"
}
Effect pav_greenShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
Effect pav_dark_green
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment_variation_dark_green"
}
Effect pav_dark_greenShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}
	


# END MOD

Effect portrait_attachment
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment"
}
Effect portrait_attachmentShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}


Effect portrait_hair
{
	VertexShader = "VS_standard"
	PixelShader = "PS_hair"
	BlendState = "alpha_blend"
	DepthStencilState = "test_and_write"
	RasterizerState = rasterizer_no_culling
}
Effect portrait_hair_opaque
{
	VertexShader = "VS_standard"
	PixelShader = "PS_hair"
	DepthStencilState = "test_and_write"
	Defines = { "ALPHA_TEST" }
}
Effect portrait_hair_opaqueShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	RasterizerState = ShadowRasterizerState
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}

Effect portrait_attachment_alpha_blend
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment"
	BlendState = "alpha_blend"
	DepthStencilState = "test_and_write"
}
Effect portrait_attachment_to_coverage
{
	VertexShader = "VS_standard"
	PixelShader = "PS_attachment"
	BlendState = "alpha_blend"
	DepthStencilState = "test_and_write"
}



Effect portrait_hairShadow
{
	VertexShader = "VertexPdxMeshStandardShadow"
	RasterizerState = ShadowRasterizerState
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	Defines = { "PDXMESH_DISABLE_DITHERED_OPACITY" }
}


Effect portrait_hair_backside
{
	VertexShader = "VS_standard"
	PixelShader = "PS_portrait_hair_backface"
	RasterizerState = rasterizer_backfaces
}
