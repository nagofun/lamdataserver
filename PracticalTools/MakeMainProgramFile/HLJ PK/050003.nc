(Laser control subs 开、关和中断光/粉子程序)
(----------------------------------------------)


%L 3000
		P200=0
		$IF [P114>=-50.0] * [P114<-49.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3200.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3250.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3000.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3100.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3050.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3150.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3200.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3250.NC
			$ENDIF
		$ELSEIF [P114>=-49.0] * [P114<-48.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3201.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3251.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3001.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3101.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3051.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3151.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3201.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3251.NC
			$ENDIF
		$ELSEIF [P114>=-48.0] * [P114<-47.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3202.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3252.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3002.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3102.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3052.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3152.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3202.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3252.NC
			$ENDIF
		$ELSEIF [P114>=-47.0] * [P114<-46.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3203.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3253.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3003.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3103.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3053.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3153.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3203.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3253.NC
			$ENDIF
		$ELSEIF [P114>=-46.0] * [P114<-45.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3204.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3254.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3004.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3104.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3054.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3154.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3204.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3254.NC
			$ENDIF
		$ELSEIF [P114>=-45.0] * [P114<-44.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3205.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3255.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3005.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3105.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3055.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3155.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3205.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3255.NC
			$ENDIF
		$ELSEIF [P114>=-44.0] * [P114<-43.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3206.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3256.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3006.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3106.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3056.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3156.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3206.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3256.NC
			$ENDIF
		$ELSEIF [P114>=-43.0] * [P114<-42.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3207.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3257.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3007.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3107.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3057.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3157.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3207.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3257.NC
			$ENDIF
		$ELSEIF [P114>=-42.0] * [P114<-41.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3208.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3258.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3008.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3108.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3058.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3158.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3208.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3258.NC
			$ENDIF
		$ELSEIF [P114>=-41.0] * [P114<-40.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3209.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3259.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3009.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3109.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3059.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3159.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3209.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3259.NC
			$ENDIF
		$ELSEIF [P114>=-40.0] * [P114<-39.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3210.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3260.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3010.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3110.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3060.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3160.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3210.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3260.NC
			$ENDIF
		$ELSEIF [P114>=-39.0] * [P114<-38.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3211.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3261.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3011.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3111.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3061.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3161.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3211.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3261.NC
			$ENDIF
		$ELSEIF [P114>=-38.0] * [P114<-37.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3212.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3262.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3012.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3112.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3062.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3162.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3212.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3262.NC
			$ENDIF
		$ELSEIF [P114>=-37.0] * [P114<-36.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3213.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3263.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3013.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3113.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3063.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3163.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3213.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3263.NC
			$ENDIF
		$ELSEIF [P114>=-36.0] * [P114<-35.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3214.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3264.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3014.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3114.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3064.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3164.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3214.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3264.NC
			$ENDIF
		$ELSEIF [P114>=-35.0] * [P114<-34.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3215.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3265.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3015.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3115.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3065.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3165.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3215.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3265.NC
			$ENDIF
		$ELSEIF [P114>=-34.0] * [P114<-33.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3216.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3266.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3016.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3116.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3066.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3166.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3216.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3266.NC
			$ENDIF
		$ELSEIF [P114>=-33.0] * [P114<-32.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3217.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3267.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3017.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3117.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3067.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3167.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3217.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3267.NC
			$ENDIF
		$ELSEIF [P114>=-32.0] * [P114<-31.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3218.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3268.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3018.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3118.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3068.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3168.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3218.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3268.NC
			$ENDIF
		$ELSEIF [P114>=-31.0] * [P114<-30.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3219.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3269.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3019.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3119.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3069.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3169.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3219.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3269.NC
			$ENDIF
		$ELSEIF [P114>=-30.0] * [P114<-29.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3220.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3270.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3020.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3120.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3070.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3170.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3220.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3270.NC
			$ENDIF
		$ELSEIF [P114>=-29.0] * [P114<-28.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3221.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3271.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3021.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3121.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3071.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3171.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3221.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3271.NC
			$ENDIF
		$ELSEIF [P114>=-28.0] * [P114<-27.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3222.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3272.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3022.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3122.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3072.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3172.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3222.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3272.NC
			$ENDIF
		$ELSEIF [P114>=-27.0] * [P114<-26.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3223.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3273.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3023.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3123.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3073.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3173.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3223.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3273.NC
			$ENDIF
		$ELSEIF [P114>=-26.0] * [P114<-25.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3224.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3274.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3024.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3124.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3074.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3174.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3224.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3274.NC
			$ENDIF
		$ELSEIF [P114>=-25.0] * [P114<-24.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3225.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3275.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3025.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3125.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3075.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3175.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3225.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3275.NC
			$ENDIF
		$ELSEIF [P114>=-24.0] * [P114<-23.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3226.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3276.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3026.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3126.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3076.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3176.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3226.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3276.NC
			$ENDIF
		$ELSEIF [P114>=-23.0] * [P114<-22.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3227.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3277.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3027.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3127.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3077.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3177.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3227.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3277.NC
			$ENDIF
		$ELSEIF [P114>=-22.0] * [P114<-21.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3228.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3278.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3028.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3128.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3078.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3178.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3228.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3278.NC
			$ENDIF
		$ELSEIF [P114>=-21.0] * [P114<-20.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3229.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3279.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3029.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3129.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3079.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3179.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3229.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3279.NC
			$ENDIF
		$ELSEIF [P114>=-20.0] * [P114<-19.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3230.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3280.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3030.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3130.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3080.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3180.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3230.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3280.NC
			$ENDIF
		$ELSEIF [P114>=-19.0] * [P114<-18.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3231.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3281.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3031.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3131.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3081.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3181.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3231.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3281.NC
			$ENDIF
		$ELSEIF [P114>=-18.0] * [P114<-17.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3232.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3282.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3032.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3132.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3082.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3182.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3232.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3282.NC
			$ENDIF
		$ELSEIF [P114>=-17.0] * [P114<-16.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3233.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3283.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3033.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3133.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3083.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3183.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3233.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3283.NC
			$ENDIF
		$ELSEIF [P114>=-16.0] * [P114<-15.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3234.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3284.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3034.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3134.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3084.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3184.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3234.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3284.NC
			$ENDIF
		$ELSEIF [P114>=-15.0] * [P114<-14.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3235.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3285.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3035.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3135.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3085.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3185.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3235.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3285.NC
			$ENDIF
		$ELSEIF [P114>=-14.0] * [P114<-13.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3236.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3286.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3036.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3136.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3086.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3186.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3236.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3286.NC
			$ENDIF
		$ELSEIF [P114>=-13.0] * [P114<-12.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3237.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3287.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3037.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3137.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3087.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3187.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3237.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3287.NC
			$ENDIF
		$ELSEIF [P114>=-12.0] * [P114<-11.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3238.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3288.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3038.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3138.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3088.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3188.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3238.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3288.NC
			$ENDIF
		$ELSEIF [P114>=-11.0] * [P114<-10.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3239.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3289.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3039.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3139.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3089.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3189.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3239.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3289.NC
			$ENDIF
		$ELSEIF [P114>=-10.0] * [P114<-9.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3240.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3290.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3040.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3140.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3090.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3190.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3240.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3290.NC
			$ENDIF
		$ELSEIF [P114>=-9.0] * [P114<-8.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3241.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3291.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3041.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3141.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3091.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3191.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3241.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3291.NC
			$ENDIF
		$ELSEIF [P114>=-8.0] * [P114<-7.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3242.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3292.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3042.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3142.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3092.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3192.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3242.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3292.NC
			$ENDIF
		$ELSEIF [P114>=-7.0] * [P114<-6.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3243.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3293.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3043.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3143.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3093.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3193.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3243.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3293.NC
			$ENDIF
		$ELSEIF [P114>=-6.0] * [P114<-5.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3244.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3294.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3044.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3144.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3094.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3194.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3244.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3294.NC
			$ENDIF
		$ELSEIF [P114>=-5.0] * [P114<-4.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3245.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3295.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3045.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3145.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3095.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3195.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3245.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3295.NC
			$ENDIF
		$ELSEIF [P114>=-4.0] * [P114<-3.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3246.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3296.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3046.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3146.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3096.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3196.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3246.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3296.NC
			$ENDIF
		$ELSEIF [P114>=-3.0] * [P114<-2.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3247.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3297.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3047.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3147.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3097.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3197.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3247.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3297.NC
			$ENDIF
		$ELSEIF [P114>=-2.0] * [P114<-1.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3248.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3298.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3048.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3148.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3098.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3198.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3248.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3298.NC
			$ENDIF
		$ELSEIF [P114>=-1.0] * [P114<0.0]
			$IF [P200==1] * [P110==1] * [P112==1]
				#CALL 3249.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==1]
				#CALL 3299.NC
			$ENDIF
			$IF [P110==1] * [P111==1]
				#CALL 3049.NC
			$ELSEIF [P110==2] * [P111==1]
				#CALL 3149.NC
			$ELSEIF [P110==1] * [P111==2]
				#CALL 3099.NC
			$ELSEIF [P110==2] * [P111==2]
				#CALL 3199.NC
			$ENDIF
			$IF [P200==1] * [P110==1] * [P112==0]
				#CALL 3249.NC
			$ELSEIF [P200==1] * [P110==2] * [P112==0]
				#CALL 3299.NC
			$ENDIF
		$ENDIF


#RET

%L 3001
	M61
	$IF [P110==1]
		$IF [P114>=-50.0] * [P114<-49.0]
			#CALL 4000.NC
		$ELSEIF [P114>=-49.0] * [P114<-48.0]
			#CALL 4001.NC
		$ELSEIF [P114>=-48.0] * [P114<-47.0]
			#CALL 4002.NC
		$ELSEIF [P114>=-47.0] * [P114<-46.0]
			#CALL 4003.NC
		$ELSEIF [P114>=-46.0] * [P114<-45.0]
			#CALL 4004.NC
		$ELSEIF [P114>=-45.0] * [P114<-44.0]
			#CALL 4005.NC
		$ELSEIF [P114>=-44.0] * [P114<-43.0]
			#CALL 4006.NC
		$ELSEIF [P114>=-43.0] * [P114<-42.0]
			#CALL 4007.NC
		$ELSEIF [P114>=-42.0] * [P114<-41.0]
			#CALL 4008.NC
		$ELSEIF [P114>=-41.0] * [P114<-40.0]
			#CALL 4009.NC
		$ELSEIF [P114>=-40.0] * [P114<-39.0]
			#CALL 4010.NC
		$ELSEIF [P114>=-39.0] * [P114<-38.0]
			#CALL 4011.NC
		$ELSEIF [P114>=-38.0] * [P114<-37.0]
			#CALL 4012.NC
		$ELSEIF [P114>=-37.0] * [P114<-36.0]
			#CALL 4013.NC
		$ELSEIF [P114>=-36.0] * [P114<-35.0]
			#CALL 4014.NC
		$ELSEIF [P114>=-35.0] * [P114<-34.0]
			#CALL 4015.NC
		$ELSEIF [P114>=-34.0] * [P114<-33.0]
			#CALL 4016.NC
		$ELSEIF [P114>=-33.0] * [P114<-32.0]
			#CALL 4017.NC
		$ELSEIF [P114>=-32.0] * [P114<-31.0]
			#CALL 4018.NC
		$ELSEIF [P114>=-31.0] * [P114<-30.0]
			#CALL 4019.NC
		$ELSEIF [P114>=-30.0] * [P114<-29.0]
			#CALL 4020.NC
		$ELSEIF [P114>=-29.0] * [P114<-28.0]
			#CALL 4021.NC
		$ELSEIF [P114>=-28.0] * [P114<-27.0]
			#CALL 4022.NC
		$ELSEIF [P114>=-27.0] * [P114<-26.0]
			#CALL 4023.NC
		$ELSEIF [P114>=-26.0] * [P114<-25.0]
			#CALL 4024.NC
		$ELSEIF [P114>=-25.0] * [P114<-24.0]
			#CALL 4025.NC
		$ELSEIF [P114>=-24.0] * [P114<-23.0]
			#CALL 4026.NC
		$ELSEIF [P114>=-23.0] * [P114<-22.0]
			#CALL 4027.NC
		$ELSEIF [P114>=-22.0] * [P114<-21.0]
			#CALL 4028.NC
		$ELSEIF [P114>=-21.0] * [P114<-20.0]
			#CALL 4029.NC
		$ELSEIF [P114>=-20.0] * [P114<-19.0]
			#CALL 4030.NC
		$ELSEIF [P114>=-19.0] * [P114<-18.0]
			#CALL 4031.NC
		$ELSEIF [P114>=-18.0] * [P114<-17.0]
			#CALL 4032.NC
		$ELSEIF [P114>=-17.0] * [P114<-16.0]
			#CALL 4033.NC
		$ELSEIF [P114>=-16.0] * [P114<-15.0]
			#CALL 4034.NC
		$ELSEIF [P114>=-15.0] * [P114<-14.0]
			#CALL 4035.NC
		$ELSEIF [P114>=-14.0] * [P114<-13.0]
			#CALL 4036.NC
		$ELSEIF [P114>=-13.0] * [P114<-12.0]
			#CALL 4037.NC
		$ELSEIF [P114>=-12.0] * [P114<-11.0]
			#CALL 4038.NC
		$ELSEIF [P114>=-11.0] * [P114<-10.0]
			#CALL 4039.NC
		$ELSEIF [P114>=-10.0] * [P114<-9.0]
			#CALL 4040.NC
		$ELSEIF [P114>=-9.0] * [P114<-8.0]
			#CALL 4041.NC
		$ELSEIF [P114>=-8.0] * [P114<-7.0]
			#CALL 4042.NC
		$ELSEIF [P114>=-7.0] * [P114<-6.0]
			#CALL 4043.NC
		$ELSEIF [P114>=-6.0] * [P114<-5.0]
			#CALL 4044.NC
		$ELSEIF [P114>=-5.0] * [P114<-4.0]
			#CALL 4045.NC
		$ELSEIF [P114>=-4.0] * [P114<-3.0]
			#CALL 4046.NC
		$ELSEIF [P114>=-3.0] * [P114<-2.0]
			#CALL 4047.NC
		$ELSEIF [P114>=-2.0] * [P114<-1.0]
			#CALL 4048.NC
		$ELSEIF [P114>=-1.0] * [P114<0.0]
			#CALL 4049.NC
		$ENDIF			
	$ELSEIF [P110==2]
		$IF [P114>=-50.0] * [P114<-49.0]
			#CALL 4500.NC
		$ELSEIF [P114>=-49.0] * [P114<-48.0]
			#CALL 4501.NC
		$ELSEIF [P114>=-48.0] * [P114<-47.0]
			#CALL 4502.NC
		$ELSEIF [P114>=-47.0] * [P114<-46.0]
			#CALL 4503.NC
		$ELSEIF [P114>=-46.0] * [P114<-45.0]
			#CALL 4504.NC
		$ELSEIF [P114>=-45.0] * [P114<-44.0]
			#CALL 4505.NC
		$ELSEIF [P114>=-44.0] * [P114<-43.0]
			#CALL 4506.NC
		$ELSEIF [P114>=-43.0] * [P114<-42.0]
			#CALL 4507.NC
		$ELSEIF [P114>=-42.0] * [P114<-41.0]
			#CALL 4508.NC
		$ELSEIF [P114>=-41.0] * [P114<-40.0]
			#CALL 4509.NC
		$ELSEIF [P114>=-40.0] * [P114<-39.0]
			#CALL 4510.NC
		$ELSEIF [P114>=-39.0] * [P114<-38.0]
			#CALL 4511.NC
		$ELSEIF [P114>=-38.0] * [P114<-37.0]
			#CALL 4512.NC
		$ELSEIF [P114>=-37.0] * [P114<-36.0]
			#CALL 4513.NC
		$ELSEIF [P114>=-36.0] * [P114<-35.0]
			#CALL 4514.NC
		$ELSEIF [P114>=-35.0] * [P114<-34.0]
			#CALL 4515.NC
		$ELSEIF [P114>=-34.0] * [P114<-33.0]
			#CALL 4516.NC
		$ELSEIF [P114>=-33.0] * [P114<-32.0]
			#CALL 4517.NC
		$ELSEIF [P114>=-32.0] * [P114<-31.0]
			#CALL 4518.NC
		$ELSEIF [P114>=-31.0] * [P114<-30.0]
			#CALL 4519.NC
		$ELSEIF [P114>=-30.0] * [P114<-29.0]
			#CALL 4520.NC
		$ELSEIF [P114>=-29.0] * [P114<-28.0]
			#CALL 4521.NC
		$ELSEIF [P114>=-28.0] * [P114<-27.0]
			#CALL 4522.NC
		$ELSEIF [P114>=-27.0] * [P114<-26.0]
			#CALL 4523.NC
		$ELSEIF [P114>=-26.0] * [P114<-25.0]
			#CALL 4524.NC
		$ELSEIF [P114>=-25.0] * [P114<-24.0]
			#CALL 4525.NC
		$ELSEIF [P114>=-24.0] * [P114<-23.0]
			#CALL 4526.NC
		$ELSEIF [P114>=-23.0] * [P114<-22.0]
			#CALL 4527.NC
		$ELSEIF [P114>=-22.0] * [P114<-21.0]
			#CALL 4528.NC
		$ELSEIF [P114>=-21.0] * [P114<-20.0]
			#CALL 4529.NC
		$ELSEIF [P114>=-20.0] * [P114<-19.0]
			#CALL 4530.NC
		$ELSEIF [P114>=-19.0] * [P114<-18.0]
			#CALL 4531.NC
		$ELSEIF [P114>=-18.0] * [P114<-17.0]
			#CALL 4532.NC
		$ELSEIF [P114>=-17.0] * [P114<-16.0]
			#CALL 4533.NC
		$ELSEIF [P114>=-16.0] * [P114<-15.0]
			#CALL 4534.NC
		$ELSEIF [P114>=-15.0] * [P114<-14.0]
			#CALL 4535.NC
		$ELSEIF [P114>=-14.0] * [P114<-13.0]
			#CALL 4536.NC
		$ELSEIF [P114>=-13.0] * [P114<-12.0]
			#CALL 4537.NC
		$ELSEIF [P114>=-12.0] * [P114<-11.0]
			#CALL 4538.NC
		$ELSEIF [P114>=-11.0] * [P114<-10.0]
			#CALL 4539.NC
		$ELSEIF [P114>=-10.0] * [P114<-9.0]
			#CALL 4540.NC
		$ELSEIF [P114>=-9.0] * [P114<-8.0]
			#CALL 4541.NC
		$ELSEIF [P114>=-8.0] * [P114<-7.0]
			#CALL 4542.NC
		$ELSEIF [P114>=-7.0] * [P114<-6.0]
			#CALL 4543.NC
		$ELSEIF [P114>=-6.0] * [P114<-5.0]
			#CALL 4544.NC
		$ELSEIF [P114>=-5.0] * [P114<-4.0]
			#CALL 4545.NC
		$ELSEIF [P114>=-4.0] * [P114<-3.0]
			#CALL 4546.NC
		$ELSEIF [P114>=-3.0] * [P114<-2.0]
			#CALL 4547.NC
		$ELSEIF [P114>=-2.0] * [P114<-1.0]
			#CALL 4548.NC
		$ELSEIF [P114>=-1.0] * [P114<0.0]
			#CALL 4549.NC
		$ENDIF
	$ENDIF
		

#RET

%L 3002
		G04 K10
		$IF [P114>=-50.0] * [P114<-49.0]
			$IF [P213==1]
				#CALL 5000.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5100.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5050.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5150.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-49.0] * [P114<-48.0]
			$IF [P213==1]
				#CALL 5001.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5101.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5051.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5151.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-48.0] * [P114<-47.0]
			$IF [P213==1]
				#CALL 5002.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5102.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5052.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5152.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-47.0] * [P114<-46.0]
			$IF [P213==1]
				#CALL 5003.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5103.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5053.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5153.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-46.0] * [P114<-45.0]
			$IF [P213==1]
				#CALL 5004.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5104.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5054.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5154.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-45.0] * [P114<-44.0]
			$IF [P213==1]
				#CALL 5005.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5105.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5055.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5155.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-44.0] * [P114<-43.0]
			$IF [P213==1]
				#CALL 5006.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5106.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5056.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5156.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-43.0] * [P114<-42.0]
			$IF [P213==1]
				#CALL 5007.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5107.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5057.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5157.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-42.0] * [P114<-41.0]
			$IF [P213==1]
				#CALL 5008.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5108.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5058.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5158.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-41.0] * [P114<-40.0]
			$IF [P213==1]
				#CALL 5009.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5109.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5059.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5159.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-40.0] * [P114<-39.0]
			$IF [P213==1]
				#CALL 5010.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5110.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5060.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5160.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-39.0] * [P114<-38.0]
			$IF [P213==1]
				#CALL 5011.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5111.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5061.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5161.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-38.0] * [P114<-37.0]
			$IF [P213==1]
				#CALL 5012.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5112.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5062.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5162.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-37.0] * [P114<-36.0]
			$IF [P213==1]
				#CALL 5013.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5113.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5063.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5163.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-36.0] * [P114<-35.0]
			$IF [P213==1]
				#CALL 5014.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5114.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5064.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5164.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-35.0] * [P114<-34.0]
			$IF [P213==1]
				#CALL 5015.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5115.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5065.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5165.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-34.0] * [P114<-33.0]
			$IF [P213==1]
				#CALL 5016.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5116.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5066.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5166.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-33.0] * [P114<-32.0]
			$IF [P213==1]
				#CALL 5017.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5117.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5067.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5167.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-32.0] * [P114<-31.0]
			$IF [P213==1]
				#CALL 5018.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5118.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5068.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5168.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-31.0] * [P114<-30.0]
			$IF [P213==1]
				#CALL 5019.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5119.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5069.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5169.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-30.0] * [P114<-29.0]
			$IF [P213==1]
				#CALL 5020.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5120.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5070.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5170.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-29.0] * [P114<-28.0]
			$IF [P213==1]
				#CALL 5021.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5121.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5071.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5171.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-28.0] * [P114<-27.0]
			$IF [P213==1]
				#CALL 5022.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5122.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5072.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5172.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-27.0] * [P114<-26.0]
			$IF [P213==1]
				#CALL 5023.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5123.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5073.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5173.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-26.0] * [P114<-25.0]
			$IF [P213==1]
				#CALL 5024.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5124.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5074.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5174.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-25.0] * [P114<-24.0]
			$IF [P213==1]
				#CALL 5025.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5125.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5075.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5175.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-24.0] * [P114<-23.0]
			$IF [P213==1]
				#CALL 5026.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5126.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5076.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5176.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-23.0] * [P114<-22.0]
			$IF [P213==1]
				#CALL 5027.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5127.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5077.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5177.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-22.0] * [P114<-21.0]
			$IF [P213==1]
				#CALL 5028.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5128.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5078.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5178.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-21.0] * [P114<-20.0]
			$IF [P213==1]
				#CALL 5029.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5129.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5079.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5179.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-20.0] * [P114<-19.0]
			$IF [P213==1]
				#CALL 5030.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5130.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5080.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5180.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-19.0] * [P114<-18.0]
			$IF [P213==1]
				#CALL 5031.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5131.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5081.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5181.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-18.0] * [P114<-17.0]
			$IF [P213==1]
				#CALL 5032.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5132.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5082.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5182.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-17.0] * [P114<-16.0]
			$IF [P213==1]
				#CALL 5033.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5133.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5083.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5183.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-16.0] * [P114<-15.0]
			$IF [P213==1]
				#CALL 5034.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5134.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5084.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5184.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-15.0] * [P114<-14.0]
			$IF [P213==1]
				#CALL 5035.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5135.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5085.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5185.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-14.0] * [P114<-13.0]
			$IF [P213==1]
				#CALL 5036.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5136.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5086.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5186.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-13.0] * [P114<-12.0]
			$IF [P213==1]
				#CALL 5037.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5137.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5087.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5187.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-12.0] * [P114<-11.0]
			$IF [P213==1]
				#CALL 5038.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5138.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5088.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5188.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-11.0] * [P114<-10.0]
			$IF [P213==1]
				#CALL 5039.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5139.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5089.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5189.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-10.0] * [P114<-9.0]
			$IF [P213==1]
				#CALL 5040.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5140.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5090.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5190.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-9.0] * [P114<-8.0]
			$IF [P213==1]
				#CALL 5041.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5141.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5091.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5191.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-8.0] * [P114<-7.0]
			$IF [P213==1]
				#CALL 5042.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5142.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5092.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5192.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-7.0] * [P114<-6.0]
			$IF [P213==1]
				#CALL 5043.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5143.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5093.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5193.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-6.0] * [P114<-5.0]
			$IF [P213==1]
				#CALL 5044.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5144.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5094.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5194.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-5.0] * [P114<-4.0]
			$IF [P213==1]
				#CALL 5045.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5145.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5095.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5195.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-4.0] * [P114<-3.0]
			$IF [P213==1]
				#CALL 5046.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5146.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5096.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5196.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-3.0] * [P114<-2.0]
			$IF [P213==1]
				#CALL 5047.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5147.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5097.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5197.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-2.0] * [P114<-1.0]
			$IF [P213==1]
				#CALL 5048.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5148.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5098.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5198.NC
				P213=1
			$ENDIF
		$ELSEIF [P114>=-1.0] * [P114<0.0]
			$IF [P213==1]
				#CALL 5049.NC
				P213=2
			$ELSEIF [P213==2]
				#CALL 5149.NC
				P213=3
			$ELSEIF [P213==3]
				#CALL 5099.NC
				P213=4
			$ELSEIF [P213==4]
				#CALL 5199.NC
				P213=1
			$ENDIF
		$ENDIF

#RET


%035006
(Part: XXX-5533220301-001-E)
(SR: MPM-CWZB-GC-022A)
(CS: SC-CT-01/02/04)
(NC: 8070)
(CX: MPM-CWZB-CX-009A)
(Pace: 10/5.0)

(Variable declaration 变量声明)
(using parameter number 使用变量号: 101~112, 115~119, 136~139, 179~185, 191~209)
(==================================================)
P102=1000 (SCANNING VELOCITY 直道扫描速率)
P104=1200 (CORNER SPD 直道为X方向时弯道扫描速率)
P103=1200 (CORNER SPD 直道为Y方向时弯道扫描速率)
P105=800 (SIDE SPD 直道为X方向时边道扫描速率)
P101=800 (SIDE SPD 直道为Y方向时边道扫描速率)
P109=2000 (IN POSITION SPD 定位移动速率)
(----------------------------------------------)
P136=800 (Color Spd Red 颜色-红色线段扫描速率)
P137=800 (Color Spd Green 颜色-绿色线段扫描速率)
P138=750 (Color Spd Blue 颜色-蓝色线段扫描速率)
P139=800 (Color Spd Yellow 颜色-黄色线段扫描速率)
(----------------------------------------------)
P181=7500 (SET LASER POWER 设定激光器功率)
P185=P181*0.78 (Controlled Laser Power 外延辅助扫描时控制激光器功率)
P184=0.5 (Laser On Stay Time 激光开光暂停时间)
P187= 15 (POWDER TIME 粉路通断停留时间)
P191=0.5(Z-INCREMENT 层提升高度)
P192=15 (IN POSITION Z UP 定位时先提Z，到位置再降Z，这一过程中Z的提升高度)
(----------------------------------------------)
P112=0 (Supplement Sup Before Fill Flag 补偿-填充前补偿标识，值取1时先进行边道补偿再走填充程序，取0时走完填充程序后再进行边道补偿)
P195=0 (SUPPLEMENT Z DOWN 	补偿-边道补偿时Z的下降高度，取正值)
P200=0 (SUPPLEMENT OUTLINE SWITCH 补偿-对外轮廓进行补偿的开关，值取1时进行边道补偿)
P115=800 (SUPPLEMENT OUTLINE SPD 补偿-对外轮廓进行补偿的扫描速率)
(----------------------------------------------)
(P110=1) (Block Type Flag 不同分块方式的标识，取值1、2。程序运行前手动设置全局变量，缺省值1)
(P111=1) (Track Type Flag 不同起点开始轨迹的标识：负搭接、轮廓扫描取值1、2；正搭接取值1、2、3、4。程序运行前手动设置全局变量，缺省值1)
(P186=60) (Cool down time 冷却时间)
P193=7 (Not used)
P179=0 (Actual Start Z 真实起始Z高度值。首次运行该程序前需确定该参数，连续执行时通常将其改为上一个程序运行完毕后的实际Z高度值，该程序一旦开始运行不应再修改该参数值)
(在模拟校验时可将P179设为V.A.PPOS.Z，这样只要Z移动范围仍位于软限位内可在任意位置进行校验)
P180=P179-0 (Delta Z 真实起始Z高度与名义起始Z高度之间的差值。)
(==================================================)
P211=4
P212=1
P213=1
P188=0
(Main program 主程序段)
(==================================================)
#PATH ["C:\CNC8070\USERS\Prg\MPM-LCX-2019-124\SUB\"]

G73 (Clear Rotation 清除可能存在的模态旋转指令)
G10 (Clear Mirror 清除可能存在的模态镜像指令)

G05



(#EXPORT)
P182=-50+P180 (START Z 根据V.A.PPOS.Z自动判断程序调用或终止-经真实起始Z高度修正后的Z高度下限)
P183=0+P180 (END Z 根据V.A.PPOS.Z自动判断程序调用或终止-经真实起始Z高度修正后的Z高度上限)
$IF [V.A.PPOS.Z >=P182] * [V.A.PPOS.Z < P183]
	$DO
		(#PREVIEW)
		P114=V.A.PPOS.Z
		$IF [V.A.PPOS.Z >=P182+10]
			P192 = 0
		$ENDIF
		SP181 M3
		M60
		G04 KP187
		#CALL 3000
		
		$IF [P212==P211]
			P212=1
			#CALL 3002			
		$ELSE			
			P212=P212+1
		$ENDIF
		
		(Change Flag)
		$IF [P110==1] * [P111==1]
			P110=2
			P111=1
		$ELSEIF [P110==2] * [P111==1]
			P110=1
			P111=2
		$ELSEIF [P110==1] * [P111==2]
			P110=2
			P111=2
		$ELSEIF [P110==2] * [P111==2]
			P110=1
			P111=1
		$ENDIF
		M61
		G04 K15
		$IF [P114>=P182] * [P114<P183-2]
			SP185 M3
			#CALL 3001
		$ENDIF
		G04 K120

		G91 G01 ZP191 FP109
		(#NEXTPREVIEW)
		
	$ENDDO V.A.PPOS.Z < P183
$ENDIF
(----------------------------------------------)

$IF [V.A.PPOS.Z >=P183] * [V.A.PPOS.Z < P183+1]
		SP181 M3
		M60
		G04 KP187
		#CALL 4049.NC
$ENDIF
(#DISEXPORT)
M61
M30
(==================================================)
