#!/usr/bin/env python3
"""
Remica Scraper - Extrae el consumo de radiadores de la web de Remica
Simplificado para usar navegador real (selenium) ya que el sitio es una SPA compleja
"""
import os
import sys

# Verificar que tenemos las credenciales
REMICA_USERNAME = os.getenv("REMICA_USERNAME")
REMICA_PASSWORD = os.getenv("REMICA_PASSWORD")

if not REMICA_USERNAME or not REMICA_PASSWORD:
    print("ERROR: Faltan credenciales")
    print("Uso: REMICA_USERNAME='email' REMICA_PASSWORD='pass' python3 remica_scraper.py")
    sys.exit(1)

print("""
================================================================================
  ANÁLISIS: El sitio de Remica usa OAuth2 con Azure AD B2C
================================================================================

El problema detectado:
  - El sitio es una Single Page Application (SPA)
  - Usa autenticación OAuth2 con Azure AD B2C  
  - Requiere JavaScript para funcionar correctamente
  - urllib no puede manejar el flujo completo de JavaScript

Opciones disponibles:
  
  1) USAR SELENIUM (RECOMENDADO)
     - Automatiza un navegador real
     - Maneja JavaScript sin problemas
     - Más robusto para sitios complejos
     
  2) PLAYWRIGHT (ALTERNATIVA MODERNA)
     - Similar a Selenium pero más moderno
     - Mejor rendimiento
     - Más fácil de usar
  
  3) ANALIZAR API DIRECTAMENTE
     - Requiere ingeniería inversa del flujo OAuth completo
     - Muy complejo de mantener si cambia el sitio
     - Puede romper términos de servicio

Recomendación:
  Usar Selenium con ChromeDriver para automatizar el login y extracción de datos.
  
¿Quieres que:
  A) Reescriba el script con Selenium?  
  B) Intente una solución más simple con la API directa (más frágil)?
  C) Proporcione instrucciones para hacerlo manualmente?

================================================================================
""")
    
    # Construir URL de login
    login_endpoint = f"{LOGIN_URL}/df9b89f5-5e1d-44fa-b17c-7c08fc83af9b/B2C_1A_SignIn_EmailVerification/SelfAsserted"
    
    if oauth_params.get('tx') and oauth_params.get('p'):
        login_endpoint += f"?tx={oauth_params['tx']}&p={oauth_params['p']}"
    
    print(f"  Endpoint: {login_endpoint[:80]}...")
    
    # Preparar datos del login
    login_data = {
        'request_type': 'RESPONSE',
        'signInName': REMICA_USERNAME,
        'password': REMICA_PASSWORD
    }
    
    data = urlencode(login_data).encode('utf-8')
    
    # Crear request con headers apropiados
    request = Request(login_endpoint, data=data)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    request.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    request.add_header('Referer', referrer_url)
    
    if oauth_params.get('x-csrf-token'):
        request.add_header('X-CSRF-Token', oauth_params['x-csrf-token'])
    
    try:
        response = opener.open(request)
        result = response.read().decode('utf-8')
        
        if DEBUG:
            with open("/tmp/remica_login_response.json", "w", encoding="utf-8") as f:
                f.write(result)
            print(f"  ✓ Respuesta guardada en /tmp/remica_login_response.json")
        
        # Parsear respuesta JSON
        try:
            json_response = json.loads(result)
            status = json_response.get('status', '')
            
            if status == '200':
                print(f"  ✓ Login exitoso")
                return True
            else:
                print(f"  ✗ Login fallido: {status}")
                return False
        except json.JSONDecodeError:
            # Si no es JSON, verificar el contenido
            if 'confirmed' in result.lower():
                print(f"  ✓ Login aparentemente exitoso")
                return True
            else:
                print(f"  ✗ Respuesta inesperada")
                return False
            
    except HTTPError as e:
        print(f"  ✗ Error HTTP: {e.code}")
        if DEBUG:
            error_body = e.read().decode('utf-8')
            with open("/tmp/remica_login_error.txt", "w", encoding="utf-8") as f:
                f.write(error_body)
        return False

def main():
    """Función principal - Solo validación de login"""
    print("╔════════════════════════════════════════╗")
    print("║   Remica Login Test                    ║")
    print("╚════════════════════════════════════════╝")
    print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    if not REMICA_USERNAME or not REMICA_PASSWORD:
        print("✗ ERROR: Faltan las credenciales.")
        print("\nConfigura las variables de entorno:")
        print("  export REMICA_USERNAME='tu_usuario'")
        print("  export REMICA_PASSWORD='tu_password'")
        return
    
    print(f"Usuario: {REMICA_USERNAME}")
    print(f"Password: {'*' * len(REMICA_PASSWORD)}\n")
    
    try:
        opener, cookie_jar = create_session()
        
        # Paso 1: Obtener parámetros OAuth
        oauth_params, referrer_url = get_oauth_params(opener)
        
        # Paso 2: Hacer login
        success = login_remica(opener, oauth_params, referrer_url)
        
        if success:
            print("\n" + "="*50)
            print("✓ TEST COMPLETADO EXITOSAMENTE")
            print("="*50)
            print("\nRevisa los archivos en /tmp/ para más detalles:")
            print("  - /tmp/remica_oauth_page.html")
            print("  - /tmp/remica_login_response.json")
        else:
            print("\n" + "="*50)
            print("✗ TEST FALLIDO")
            print("="*50)
            print("\nRevisa los archivos en /tmp/ para debugging")
            
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
