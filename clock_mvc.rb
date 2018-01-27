require "observer"

class WatchModel
    include Observable
    def initialize
        @running = false
        @time = 0
        @last = 0.0
        Thread.start do
            loop do
                sleep 0.01
                if @running
                    now = Time.now.to_f
                    @time += now - @last
                    @last = now
                    changed
                    notify_observers(@time)
                end
            end
        end
    end
    
    def start_stop
        @last = Time.now.to_f
        @running = ! @running
    end

    def time
        @time
    end
end

class WatchView
    def initialize(model)
        model.add_observer(self)
    end
    
    def update(time)
        printf "%02d:%02d\n", time.to_i, (time - time.to_i)*100
        STDOUT.flush
    end
end

class WatchController
    def initialize
        @model = WatchModel.new
        @view = WatchView.new(@model)
        # system "stty cbreak -echo"

        begin
            @view.update(@model.time)
            loop do
                if STDIN.getc == ?q
                    break
                end
                @model.start_stop
            end
        ensure
            # system "stty cooked echo"
        end
    end
end

WatchController.new