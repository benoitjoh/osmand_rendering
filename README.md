# osmand_rendering
rendering files for osmand app


#lines


##simple line

color="#ffffff" 
strokeWidth="6"

--> white line 6 broad

## line with colored border
color="#ffffff" color_0="#837DF6" 
strokeWidth="4" strokeWidth_0="6"

--> white line (4) over a blue line (6)


color="#ffffff" color_0="#837DF6" 
strokeWidth="4" strokeWidth_0="4:5" pathEffect="4_12"



        <!--
        <switch>
            <case tag="highway" value="track"/>
            <apply color="#ffffff"  color_0="#837DF6" order="2"/> 
            <groupFilter>
                <filter maxzoom="16" strokeWidth="4" strokeWidth_0="4:5" pathEffect="8_24"/>
                <filter minzoom="16" strokeWidth="8" strokeWidth_0="8:9" pathEffect="12_36"/>
            
        
            </groupFilter>
        </switch>
        -->
