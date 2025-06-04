from julep import Client
import time
import yaml
from datetime import datetime

JULEP_API_KEY = "api_key"

def create_food_tour(cities_list):
    """
    Create a comprehensive food tour for the given cities.
    
    Args:
        cities_list (list): List of cities to create food tours for
    
    Returns:
        str: Generated food tour guide
    """
    
    # Initialize the client
    client = Client(api_key=JULEP_API_KEY)
    
    # Create the food tour agent
    agent = client.agents.create(
        name="Julep Food Tour Expert",
        model="claude-3.7-sonnet",
        about="A world-renowned food critic and travel expert who creates exceptional food experiences, specializing in weather-optimized dining recommendations and authentic local cuisine discovery.",
    )
    
    # Load the food task definition
    with open('food_task.yaml', 'r', encoding='utf-8') as file:
        task_definition = yaml.safe_load(file)
    
    # Create the task
    task = client.tasks.create(
        agent_id=agent.id,
        **task_definition
    )
    
    # Create the execution
    execution = client.executions.create(
        task_id=task.id,
        input={
            "cities": cities_list
        }
    )
    
    print("🍽️ Creating your ultimate food tour...")
    print(f"📍 Cities: {', '.join(cities_list)}")
    print("⏳ Processing...")
    
    step_count = 0
    while (result := client.executions.get(execution.id)).status not in ['succeeded', 'failed']:
        step_count += 1
        
        # Get detailed execution information
        try:
            execution_details = client.executions.get(execution.id)
            
            # Create progress messages based on step count
            if step_count <= 3:
                print(f"🌤️  Step {step_count}: Checking weather conditions...")
            elif step_count <= 6:
                print(f"🥘 Step {step_count}: Researching iconic local dishes...")
            elif step_count <= 9:
                print(f"🏪 Step {step_count}: Finding top-rated restaurants...")
            elif step_count <= 12:
                print(f"📚 Step {step_count}: Gathering food culture insights...")
            else:
                print(f"✨ Step {step_count}: Crafting your personalized food experience...")
            
            # Show any available progress details
            if hasattr(execution_details, 'steps') and execution_details.steps:
                completed_steps = len([s for s in execution_details.steps if hasattr(s, 'status') and s.status == 'completed'])
                total_steps = len(execution_details.steps)
                if total_steps > 0:
                    progress_percent = int((completed_steps / total_steps) * 100)
                    print(f"   Progress: {completed_steps}/{total_steps} ({progress_percent}%)")
                    
        except Exception as e:
            print(f"   (Processing: {str(e)[:50]}...)")
        
        time.sleep(3) 
    
    print(f"\n🎉 Food tour creation completed with status: {result.status}")
      # Process the result
    if result.status == "succeeded":
        # Extract the final food guide from the result output
        if hasattr(result, 'output') and result.output:
            if isinstance(result.output, dict):
                if 'final_food_guide' in result.output:
                    formatted_output = result.output['final_food_guide']
                else:
                    # Return the last step output or full output
                    formatted_output = str(result.output)
            else:
                formatted_output = str(result.output)
        else:
            formatted_output = "Tour created successfully but output format unexpected."
        
        return formatted_output
    else:
        error_msg = f"❌ Error creating food tour: {getattr(result, 'error', 'Unknown error occurred')}"
        print(error_msg)
        return error_msg

def main():
    """
    Main function to run the food tour creator.
    """
    print("🍽️ Welcome to the Ultimate Food Tour Creator!")
    cities = [
        "Kozhikode",
        "Malappuram",
        "Kochi"
    ]
    
    # Create the food tour
    try:
        food_guide = create_food_tour(cities)
        
        # Save the result to a file
        filename = f'ultimate_food_tour_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(food_guide)
        
        print(f"\n📁 Your ultimate food tour has been saved to: {filename}")
        print("\n🎯 Preview of your food adventure:")
        print("-" * 60)
        # Show first 500 characters as preview
        print(food_guide[:500] + "...\n")
        print(f"💡 Open {filename} to see your complete food tour!")
        
    except Exception as e:
        error_msg = f"❌ An error occurred: {str(e)}"
        print(error_msg)
        
        # Save error log
        error_filename = f'food_tour_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(error_filename, 'w', encoding='utf-8') as f:
            f.write(error_msg)
        print(f"Error details saved to: {error_filename}")

if __name__ == "__main__":
    main()
