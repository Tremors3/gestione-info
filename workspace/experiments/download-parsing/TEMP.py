@staticmethod
    def _parse_page(html_content: str) -> Optional[Dict]:
        """Effettua il parsing del contenuto HTML in un dizionario."""
        # Sostituire con una logica di parsing reale
        try:
            
            parsed_data = {}
            
            for meta in soup.find_all('meta'):
                parsed_data[meta.get('name')] = meta['content']
            
            parsed_data = {"content": html_content[:200], "length": len(html_content)}  # Esempio
            return parsed_data
        
        
        
        
        except Exception as e:
            logging.warning(f"Errore durante il parsing del contenuto HTML: {e}")
            return None