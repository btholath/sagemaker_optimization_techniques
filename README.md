# sagemaker_optimization_techniques
Explore a comprehensive guide to Amazon SageMaker optimization techniques including hyperparameter tuning, model compilation, distributed training, and deployment strategies. Ideal for ML engineers aiming to streamline performance in scalable machine learning workflows.



# 1. Create AWS resources
python -m bayesian.resource_setup.create_resources

# 2. Generate synthetic data
python -m bayesian.consumer_spending.preprocessing.generate_data

# 3. Upload data to S3
python -m bayesian.consumer_spending.preprocessing.upload_to_s3

# 4. Run local Bayesian Optimization
python -m bayesian.consumer_spending.tuning.bayesian_optimization

# 5. Run SageMaker hyperparameter tuning
python -m bayesian.consumer_spending.sagemaker.sagemaker_bayesian_tuning

# 6. Plot convergence from optimization results
python -m bayesian.consumer_spending.visualization.plot_convergence