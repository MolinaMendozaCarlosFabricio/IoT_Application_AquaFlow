def CalculateWaterActivities(ph, tds, ntu, amqpManager):
    activities = []

    # Riego de plantas
    if ntu <= 20.0 and tds <= 1500 and ph > 6 and ph < 9:
        calculate_ntu = 20.0 - ph
        if calculate_ntu < 0:
            calculate_ntu = 0
        calculate_tds = 1500 - tds
        if calculate_tds < 0:
            calculate_tds = 0
        calculate_ph = 7.5 - ph
        if calculate_ph < -1.5 or calculate_ph > 1.5:
            calculate_ph = 0
        if calculate_ph < 0:
            calculate_ph *= -1
        
        ntu_p = (calculate_ntu/20.0) * 100
        tds_p = (calculate_tds/1500) * 100
        ph_p = (calculate_ph/1.5) * 100

        p = (ntu_p + tds_p + ph_p) / 3
        activities.append({
            "water_activity": "Riego de plantas",
            "percentage": p,
        })
    
    # Lavar el coche
    if ntu <= 40.0 and tds <= 1200 and ph > 5.5 and ph < 9.5:
        calculate_ntu = 40.0 - ph
        if calculate_ntu < 0:
            calculate_ntu = 0
        calculate_tds = 1200 - tds
        if calculate_tds < 0:
            calculate_tds = 0
        calculate_ph = 7.5 - ph
        if calculate_ph < -2 or calculate_ph > 2:
            calculate_ph = 0
        if calculate_ph < 0:
            calculate_ph *= -1
        
        ntu_p = (calculate_ntu/40.0) * 100
        tds_p = (calculate_tds/1200) * 100
        ph_p = (calculate_ph/2) * 100 

        p = (ntu_p + tds_p + ph_p) / 3
        activities.append({
            "water_activity": "Lavar auto",
            "percentage": p,
        })
    
    # Limpieza del hogar
    if ntu <= 60.0 and tds <= 1500 and ph > 5.5 and ph < 9.5:
        calculate_ntu = 60.0 - ph
        if calculate_ntu < 0:
            calculate_ntu = 0
        calculate_tds = 1500 - tds
        if calculate_tds < 0:
            calculate_tds = 0
        calculate_ph = 7.5 - ph
        if calculate_ph < -2 or calculate_ph > 2:
            calculate_ph = 0
        if calculate_ph < 0:
            calculate_ph *= -1
        
        ntu_p = (calculate_ntu/60) * 100
        tds_p = (calculate_tds/1500) * 100
        ph_p = (calculate_ph/2) * 100 

        p = (ntu_p + tds_p + ph_p) / 3
        activities.append({
            "water_activity": "Limpieza del hogar (pisos y exteriores)",
            "percentage": p,
        })
    
    # Lavado de ropa
    if ntu <= 20.0 and tds <= 800 and ph > 6 and ph < 9:
        calculate_ntu = 20.0 - ph
        if calculate_ntu < 0:
            calculate_ntu = 0
        calculate_tds = 800 - tds
        if calculate_tds < 0:
            calculate_tds = 0
        calculate_ph = 7.5 - ph
        if calculate_ph < -1.5 or calculate_ph > 1.5:
            calculate_ph = 0
        if calculate_ph < 0:
            calculate_ph *= -1
        
        ntu_p = (calculate_ntu/20) * 100
        tds_p = (calculate_tds/800) * 100
        ph_p = (calculate_ph/1.5) * 100 

        p = (ntu_p + tds_p + ph_p) / 3
        activities.append({
            "water_activity": "Lavado de ropa",
            "percentage": p,
        })

    # Descarga de inodoros
    if ntu <= 100.0 and tds <= 3000 and ph > 5.0 and ph < 9.5:
        calculate_ntu = 100.0 - ph
        if calculate_ntu < 0:
            calculate_ntu = 0
        calculate_tds = 3000 - tds
        if calculate_tds < 0:
            calculate_tds = 0
        calculate_ph = 7.25 - ph
        if calculate_ph < -2.25 or calculate_ph > 2.25:
            calculate_ph = 0
        if calculate_ph < 0:
            calculate_ph *= -1
        
        ntu_p = (calculate_ntu/100) * 100
        tds_p = (calculate_tds/3000) * 100
        ph_p = (calculate_ph/2.25) * 100 

        p = (ntu_p + tds_p + ph_p) / 3
        activities.append({
            "water_activity": "Descarga de inodoros",
            "percentage": p,
        })

    # Lavado de calles o banquetas
    if ntu <= 200.0 and tds <= 1500 and ph > 5.5 and ph < 9.5:
        calculate_ntu = 200.0 - ph
        if calculate_ntu < 0:
            calculate_ntu = 0
        calculate_tds = 1500 - tds
        if calculate_tds < 0:
            calculate_tds = 0
        calculate_ph = 7.5 - ph
        if calculate_ph < -2 or calculate_ph > 2:
            calculate_ph = 0
        if calculate_ph < 0:
            calculate_ph *= -1
        
        ntu_p = (calculate_ntu/200) * 100
        tds_p = (calculate_tds/1500) * 100
        ph_p = (calculate_ph/2) * 100 

        p = (ntu_p + tds_p + ph_p) / 3
        activities.append({
            "water_activity": "Lavado de calles o banquetas",
            "percentage": p,
        })

        try:
            amqpManager.publishMessage("websocket_topic.water_activities", activities)
            print("Enviando actividades con el agua")
        except Exception as e:
            print("Error al mandar actividades del agua por amqp:", e)
        
        return activities
