#!/usr/bin/env python3
"""
Test XML Generation Function
"""

def test_xml_generation():
    """Test if XML generation is working correctly"""
    
    print("🧪 Testing XML Generation")
    print("=" * 30)
    
    try:
        from api.exotel_webhook import create_exotel_response
        
        # Test with a simple message
        test_message = "Hello! Welcome to NextCore AI. How can I help you today?"
        xml = create_exotel_response(test_message)
        
        print(f"✅ XML Generated: {len(xml)} characters")
        print(f"✅ Contains <?xml: {'<?xml' in xml}")
        print(f"✅ Contains <Response>: {'<Response>' in xml}")
        print(f"✅ Contains <Say>: {'<Say>' in xml}")
        print(f"✅ Contains <Gather>: {'<Gather' in xml}")
        
        print(f"\n📄 Sample XML:")
        print(xml[:200] + "..." if len(xml) > 200 else xml)
        
        # Validate XML structure
        required_tags = ['<?xml', '<Response>', '<Say>', '<Gather', '</Response>']
        all_present = all(tag in xml for tag in required_tags)
        
        if all_present:
            print("\n🎉 XML Generation is working perfectly!")
            return True
        else:
            print("\n❌ XML is missing some required tags")
            return False
            
    except Exception as e:
        print(f"❌ Error testing XML: {e}")
        return False

if __name__ == "__main__":
    test_xml_generation()
