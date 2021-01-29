require_relative 'lib/simp/test/version'

Gem::Specification.new do |spec|
  spec.name          = "simp-test"
  spec.version       = Simp::Test::VERSION
  spec.authors       = ["SIMP Team"]
  spec.email         = ["info@simp-project.com"]

  spec.summary       = %q{test gem for CI}
  spec.homepage      = "https://github.com/simp/rubygem-simp-test"
  spec.required_ruby_version = Gem::Requirement.new(">= 2.3.0")

  spec.metadata["allowed_push_host"] = "TODO: Set to 'http://mygemserver.com'"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = "https://github.com/simp/rubygem-simp-test"
  spec.metadata["changelog_uri"] = "https://github.com/simp/rubygem-simp-test/blob/master/CHANGELOG.md"

  # Specify which files should be added to the gem when it is released.
  # The `git ls-files -z` loads the files in the RubyGem that have been added into git.
  spec.files         = Dir.chdir(File.expand_path('..', __FILE__)) do
    `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  end
  spec.bindir        = "exe"
  spec.executables   = spec.files.grep(%r{^exe/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]
end
