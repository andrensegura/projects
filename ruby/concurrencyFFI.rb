require 'rubygems'
require 'ffi'

module Hello
  extend FFI::Library
  ffi_lib '/home/andre/projects/rust/embed/target/release/libembed.so'
  attach_function :process, [], :void
end

Hello.process

puts 'done!'
